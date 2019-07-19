package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
	"time"

	"git.beryju.org/BeryJu.org/p2/tier0/internal"
	p2client "git.beryju.org/BeryJu.org/p2/tier0/internal/protos"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/cache"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/k8s"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/metrics"
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
	grpcClusterIP := "localhost"
	if err != nil {
		log.Warning(err)
	} else {
		grpcClusterIP, err = k8sc.GetGRPCClusterIP()
		if err != nil {
			log.Warning(err)
			log.Debugf("Falling back to default GRPC ClusterIP %s", grpcClusterIP)
		}
	}
	// Central stopping channel
	stop := make(chan struct{})
	upstream := p2.NewGRPCUpstream(fmt.Sprintf("%s:50051", grpcClusterIP))
	localCache := cache.NewCache(upstream)
	localCache.SetPeersFromKubernetes(k8sc)
	// Update Cache Peers by watching k8s
	go k8sc.WatchNewCachePods(stop, func(pod v1.Pod) {
		localCache.SetPeersFromKubernetes(k8sc)
	})
	go localCache.StartCacheServer()
	go localCache.StartMetricsTimer()
	go metrics.StartServer()
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
		key := cache.RequestFingerprint(*r)
		context := cache.CacheContext{
			RequestHeader: r.Header,
			Host:          r.Host,
			Request:       *r,
		}
		var reply p2client.ServeReply
		err := localCache.Group.Get(context, key, groupcache.ProtoSink(&reply))
		if err != nil {
			log.Warn(err)
		}
		for headerKey, headerValue := range reply.Headers {
			w.Header().Set(headerKey, headerValue)
		}
		if reply.Matching {
			http.ServeContent(w, r, "", time.Now(), bytes.NewReader(reply.Data))
		} else {
			fmt.Fprintf(w, "blob not found")
		}
	}
	mainServer.Handle("/", handlers.LoggingHandler(os.Stdout, http.HandlerFunc(mainServerHandler)))
	err = http.ListenAndServe(constants.Listen, mainServer)
	if err != nil {
		log.Fatal(err)
	}
	defer close(stop)
}
