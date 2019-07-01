package metrics

import (
	"net/http"

	"git.beryju.org/BeryJu.org/p2/tier0/pkg/constants"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	log "github.com/sirupsen/logrus"
)

func StartServer() {
	// create a new mux server
	server := http.NewServeMux()
	// register a new handler for the /metrics endpoint
	server.Handle("/metrics", promhttp.Handler())
	// start an http server using the mux server
	log.Printf("Running Metrics server on %s...", constants.ListenMetrics)
	http.ListenAndServe(constants.ListenMetrics, server)
}
