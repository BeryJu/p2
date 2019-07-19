package cache

import (
	"crypto/sha256"
	"fmt"
	"net"
	"net/http"
	"os"
	"strings"
	"time"

	"git.beryju.org/BeryJu.org/p2/tier0/pkg/metrics"

	"github.com/prometheus/client_golang/prometheus"

	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/k8s"
	"git.beryju.org/BeryJu.org/p2/tier0/pkg/p2"

	"github.com/qbig/groupcache"
	log "github.com/sirupsen/logrus"
)

var (
	getsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_gets",
		Help: "any Get request, including from peers",
	})
	cacheHitsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_hits",
		Help: "either cache was good",
	})
	peerLoadsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_peer_loads",
		Help: "either remote load or remote cache hit (not an error)",
	})
	peerErrorsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_peer_errors",
		Help: "",
	})
	loadsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_loads",
		Help: "(gets - cacheHits)",
	})
	loadsDedupedMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_loads_deduped",
		Help: "after singleflight",
	})
	localLoadsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_local_loads",
		Help: "total good local loads",
	})
	localLoadsErrMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_local_loads_err",
		Help: "total bad local loads",
	})
	serverRequestsMetric = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cache_server_requests",
		Help: "gets that came over the network from peers",
	})
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
	// request.Header.Del("If-Modified-Since")
	// log.Debugf("Fingerprinting request on headers '%s'", reflect.ValueOf(request.Header).MapKeys())
	// log.Debug(request.Header)
	// fingerprintData[2] = fmt.Sprintf("%x", sha256.Sum256([]byte(fmt.Sprintf("%s", request.Header))))
	fingerprintData[2] = ""
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
			if err != nil {
				logger.Warnf("Error fetching blob: %s", err)
			}
			dest.SetProto(blob)
			return nil
		}))
	// We save our local IP to prevent endless circles
	hostname, err := os.Hostname()
	if err != nil {
		logger.Warn(err)
	}
	ip, err := net.LookupHost(hostname)
	if err != nil {
		logger.Warn(err)
	}
	pool := groupcache.NewHTTPPool(fmt.Sprintf("http://%s%s", ip[0], constants.ListenCache))
	// Setup prometheus
	prometheus.MustRegister(getsMetric)
	prometheus.MustRegister(cacheHitsMetric)
	prometheus.MustRegister(peerLoadsMetric)
	prometheus.MustRegister(peerErrorsMetric)
	prometheus.MustRegister(loadsMetric)
	prometheus.MustRegister(loadsDedupedMetric)
	prometheus.MustRegister(localLoadsMetric)
	prometheus.MustRegister(localLoadsErrMetric)
	prometheus.MustRegister(serverRequestsMetric)
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
	c.Logger.Infof("Running Cache-Peer server on %s...", constants.ListenCache)
	http.ListenAndServe(constants.ListenCache, metrics.RequestLogger(c.Logger, cacheServer))
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

// StartMetricsTimer Start timer which updates Metrics every 5 seconds
func (c *Cache) StartMetricsTimer() {
	for range time.NewTicker(5 * time.Second).C {
		c.UpdateMetrics()
	}
}

// UpdateMetrics Update prometheus metrics from current cache
func (c *Cache) UpdateMetrics() {
	stats := c.Group.Stats
	getsMetric.Set(float64(stats.Gets))
	cacheHitsMetric.Set(float64(stats.CacheHits))
	peerLoadsMetric.Set(float64(stats.PeerLoads))
	peerErrorsMetric.Set(float64(stats.PeerErrors))
	loadsMetric.Set(float64(stats.Loads))
	loadsDedupedMetric.Set(float64(stats.LoadsDeduped))
	localLoadsMetric.Set(float64(stats.LocalLoads))
	localLoadsErrMetric.Set(float64(stats.LocalLoadErrs))
	serverRequestsMetric.Set(float64(stats.ServerRequests))
}
