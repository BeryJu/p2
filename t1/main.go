package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"time"

	"git.beryju.org/BeryJu.org/t1/pkg/constants"

	"git.beryju.org/BeryJu.org/t1/pkg/k8s"

	"git.beryju.org/BeryJu.org/t1/pkg/cache"
	v1 "k8s.io/api/core/v1"

	"git.beryju.org/BeryJu.org/t1/pkg/p2"
	"github.com/gorilla/handlers"
	"github.com/qbig/groupcache"
	log "github.com/sirupsen/logrus"
)

func main() {
	log.SetLevel(log.DebugLevel)
	log.Debug("Starting p2-tier1")
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
	upstream := p2.Upstream{URL: fmt.Sprintf("http://%s", webClusterIP)}
	cache := cache.NewCache(upstream)
	cache.SetPeersFromK8s(k8sc)
	// Update Cache Peers by watching k8s
	go k8sc.WatchNewCachePods(stop, func(pod v1.Pod) {
		cache.SetPeersFromK8s(k8sc)
	})
	go cache.StartCacheServer()
	groupcache.RegisterErrLogHook(func(err error) {
		log.Warning(err)
	})
	log.Printf("Running on %s...", constants.Listen)
	http.HandleFunc("/_/t1/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	})
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		var data []byte
		escapedPath := url.QueryEscape(r.URL.Path)
		err := cache.Group.Get(nil, escapedPath, groupcache.AllocatingByteSliceSink(&data))
		if err != nil {
			log.Fatal(err)
		}
		http.ServeContent(w, r, "", time.Now(), bytes.NewReader(data))
	})
	err = http.ListenAndServe(constants.Listen, handlers.LoggingHandler(os.Stdout, http.DefaultServeMux))
	if err != nil {
		log.Fatal(err)
	}
	defer close(stop)
}
