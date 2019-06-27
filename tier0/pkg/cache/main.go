package cache

import (
	"fmt"
	"net"
	"net/http"
	"os"

	"github.com/gorilla/handlers"

	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/k8s"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/p2"

	"github.com/qbig/groupcache"
	log "github.com/sirupsen/logrus"
)

type Cache struct {
	Group    *groupcache.Group
	Logger   *log.Entry
	Pool     *groupcache.HTTPPool
	hostname string
	localIP  string
}

type CacheContext struct {
	groupcache.Context
	RequestHeader http.Header
}

func NewCache(upstream p2.Upstream) Cache {
	logger := log.WithFields(log.Fields{
		"component": "cache",
	})
	cache := groupcache.NewGroup("tier0", constants.CacheSize, groupcache.GetterFunc(
		func(_ctx groupcache.Context, key string, dest groupcache.Sink) error {
			ctx := _ctx.(CacheContext)
			logger.Debug("Fetching key from upstream...")
			blob, err := upstream.Fetch(ctx.RequestHeader, key)
			if err == nil {
				dest.SetBytes(blob.Data)
			} else {
				logger.Debugf("Error fetching blob: %s", err)
			}
			return nil
		}))
	// We save our local IP to prevent endless circles
	hostname, err := os.Hostname()
	if err != nil {
		logger.Debug(err)
	}
	ip, err := net.LookupHost(hostname)
	if err != nil {
		logger.Debug(err)
	}
	pool := groupcache.NewHTTPPool(fmt.Sprintf("http://%s%s", ip[0], constants.ListenCache))
	return Cache{
		Group:    cache,
		Logger:   logger,
		Pool:     pool,
		hostname: hostname,
		localIP:  ip[0],
	}
}

func (c *Cache) StartCacheServer() {
	cacheServer := http.NewServeMux()
	cacheServer.HandleFunc("/_groupcache/", c.Pool.ServeHTTP)
	log.Infof("Running Cache-Peer server on %s...", constants.ListenCache)
	http.ListenAndServe(constants.ListenCache, handlers.LoggingHandler(os.Stdout, cacheServer))
}

func (c *Cache) SetPeersFromK8s(k8sc k8s.KubernetesContext) {
	pods := k8sc.PodsForComponent("cache")
	podAddresses := make([]string, 0)
	for _, element := range pods.Items {
		if element.Status.PodIP != "" {
			podURL := fmt.Sprintf("http://%s%s", element.Status.PodIP, constants.ListenCache)
			podAddresses = append(podAddresses, podURL)
		}
	}
	if len(podAddresses) > 0 {
		c.Pool.Set(podAddresses...)
		c.Logger.Debugf("Set Peers to %s", podAddresses)
	}
}
