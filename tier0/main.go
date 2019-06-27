package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"time"

	"git.beryju.org/BeryJu.org/p2/tier0/internal"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/cache"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/k8s"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/p2"

	"github.com/gorilla/handlers"
	"github.com/qbig/groupcache"
	log "github.com/sirupsen/logrus"
	v1 "k8s.io/api/core/v1"
)

func main() {
	log.SetLevel(log.DebugLevel)
	log.Debugf("Starting p2-tier0 Version %s", internal.Version)
	k8sc, err := k8s.NewKubernetesContext()
	if err != nil {
		log.Fatal(err)
	}
	webClusterIP, err := k8sc.WebClusterIP()
	if err != nil {
		log.Fatal(err)
	}
	// Central stopping channel
	stop := make(chan struct{})
	upstream := p2.NewUpstream(fmt.Sprintf("http://%s", webClusterIP))
	localCache := cache.NewCache(upstream)
	localCache.SetPeersFromK8s(k8sc)
	// Update Cache Peers by watching k8s
	go k8sc.WatchNewCachePods(stop, func(pod v1.Pod) {
		localCache.SetPeersFromK8s(k8sc)
	})
	go localCache.StartCacheServer()
	groupcache.RegisterErrLogHook(func(err error) {
		log.Warning(err)
	})
	log.Printf("Running on %s...", constants.Listen)
	// Create main HTTP Server
	mainServer := http.NewServeMux()
	mainServer.HandleFunc("/_/tier0/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	})
	mainServerHandler := func(w http.ResponseWriter, r *http.Request) {
		var data []byte
		escapedPath := url.QueryEscape(r.URL.Path)
		context := cache.CacheContext{
			RequestHeader: r.Header,
			Host:          r.Host,
		}
		err := localCache.Group.Get(context, escapedPath, groupcache.AllocatingByteSliceSink(&data))
		if err != nil {
			log.Fatal(err)
		}
		http.ServeContent(w, r, "", time.Now(), bytes.NewReader(data))
	}
	mainServer.Handle("/", handlers.LoggingHandler(os.Stdout, http.HandlerFunc(mainServerHandler)))
	err = http.ListenAndServe(constants.Listen, mainServer)
	if err != nil {
		log.Fatal(err)
	}
	defer close(stop)
}
