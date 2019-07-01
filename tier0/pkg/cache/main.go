package cache

import (
	"crypto/sha256"
	"fmt"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gorilla/handlers"

	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/k8s"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/p2"

	"github.com/mitchellh/hashstructure"
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
	Request       http.Request
	RequestHeader http.Header
	Host          string
}

// RequestFingerprint Return a unique fingerprint to identify requests
func RequestFingerprint(request http.Request) string {
	fingerprintData := make([]string, 3)
	fingerprintData[0] = request.URL.String()
	// Since we don't know the user here, we use the session (or try to)
	session, err := request.Cookie("sessionid")
	if err == nil {
		fingerprintData[1] = session.Value
	} else {
		fingerprintData[1] = ""
	}
	hash, err := hashstructure.Hash(request.Header, nil)
	if err == nil {
		fingerprintData[2] = strconv.FormatUint(hash, 10)
	} else {
		fingerprintData[2] = ""
	}
	fullHash := sha256.Sum256([]byte(strings.Join(fingerprintData, "")))
	return fmt.Sprintf("%x", fullHash)
}

// NewCache Instantiate new Cache Group and HTTP Peer Pool
func NewCache(upstream p2.GRPCUpstream) Cache {
	logger := log.WithFields(log.Fields{
		"component": "cache",
	})
	cache := groupcache.NewGroup("tier0", constants.CacheSize, groupcache.GetterFunc(
		func(_ctx groupcache.Context, key string, dest groupcache.Sink) error {
			if _ctx == nil {
				logger.Warningf("Empty context for key '%s'", key)
				return nil
			}
			ctx := _ctx.(CacheContext)
			logger.Debugf("Fetching upstream key '%s'", key)
			blob, err := upstream.Fetch(ctx.Request)
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

// StartCacheServer Start Cache Peer server (blocking)
func (c *Cache) StartCacheServer() {
	cacheServer := http.NewServeMux()
	cacheServer.HandleFunc("/_groupcache/", c.Pool.ServeHTTP)
	log.Infof("Running Cache-Peer server on %s...", constants.ListenCache)
	http.ListenAndServe(constants.ListenCache, handlers.LoggingHandler(os.Stdout, cacheServer))
}

// SetPeersFromKubernetes Attempt to autodiscover all tier0 pods and connect to them.
func (c *Cache) SetPeersFromKubernetes(k8sc k8s.KubernetesContext) {
	pods := k8sc.PodsForComponent("tier0")
	if pods == nil {
		c.Logger.Debug("No pods found or connetion issue.")
		return
	}
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
