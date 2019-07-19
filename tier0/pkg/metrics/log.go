package metrics

import (
	"net/http"
	"time"

	log "github.com/sirupsen/logrus"
)

func RequestLogger(logger *log.Entry, targetMux http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		targetMux.ServeHTTP(w, r)

		// log request by who(IP address)
		requesterIP := r.RemoteAddr

		logger.WithFields(log.Fields{
			"method":      r.Method,
			"from":        requesterIP,
			"duration_ms": time.Since(start) / time.Millisecond,
		}).Printf(r.RequestURI)
	})
}
