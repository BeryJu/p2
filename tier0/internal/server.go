package internal

import (
	"bytes"
	"fmt"
	"net/http"
	"time"

	p2client "git.beryju.org/BeryJu.org/p2/tier0/internal/protos"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/cache"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/k8s"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/metrics"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/p2"

	"github.com/qbig/groupcache"
	log "github.com/sirupsen/logrus"
	v1 "k8s.io/api/core/v1"
)

var mainLogger = log.WithField("component", "main")

func Main() {
	// Central stopping channel
	stop := make(chan struct{})
	// attempt to connect to k8s
	grpcClusterIP := "localhost"
	connectedToK8s := false
	k8sc, err := k8s.NewKubernetesContext()
	if err != nil {
		mainLogger.Debugf("Falling back to default GRPC ClusterIP %s", grpcClusterIP)
	} else {
		connectedToK8s = true
		grpcClusterIP, err = k8sc.GetGRPCClusterIP()
		if err != nil {
			mainLogger.Warning(err)
		}
	}
	upstream := p2.NewGRPCUpstream(fmt.Sprintf("%s:50051", grpcClusterIP))
	localCache := cache.NewCache(upstream)
	if connectedToK8s {
		localCache.SetPeersFromKubernetes(k8sc)
		// Update Cache Peers by watching k8s
		go k8sc.WatchNewCachePods(stop, func(pod v1.Pod) {
			localCache.SetPeersFromKubernetes(k8sc)
		})
	}
	go localCache.StartCacheServer()
	go localCache.StartMetricsTimer()
	go metrics.StartServer()
	groupcache.RegisterErrLogHook(func(err error) {
		mainLogger.Warning(err)
	})
	mainLogger.Printf("Running on %s...", constants.Listen)
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
			mainLogger.Warn(err)
		}
		// Location header needs special handling
		if location, ok := reply.Headers["Location"]; ok {
			http.Redirect(w, r, location, http.StatusFound)
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
	mainServer.Handle("/", metrics.RequestLogger(mainLogger, http.HandlerFunc(mainServerHandler)))
	err = http.ListenAndServe(constants.Listen, mainServer)
	if err != nil {
		mainLogger.Fatal(err)
	}
	defer close(stop)
}
