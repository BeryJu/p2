package p2

import (
	"context"
	"net"
	"net/http"
	"strings"

	p2client "git.beryju.org/BeryJu.org/p2/tier0/internal/protos"
	log "github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

// GRPCUpstream Hold internal grpc connection to upstream server. Use NewGRPCUpstream.
type GRPCUpstream struct {
	*grpc.ClientConn
	Logger      *log.Entry
	ServeClient p2client.ServeClient
}

// NewGRPCUpstream Initialise connection to upstream GRPC server
func NewGRPCUpstream(url string) GRPCUpstream {
	logger := log.WithFields(log.Fields{
		"component": "upstream",
	})
	conn, err := grpc.Dial(url, grpc.WithInsecure())
	if err != nil {
		log.Error(err)
	}
	client := p2client.NewServeClient(conn)
	logger.Debug("Successfully connected to upstream")
	return GRPCUpstream{conn, logger, client}
}

func (u *GRPCUpstream) headersToDjango(request http.Request) map[string]string {
	newHeaders := make(map[string]string, 0)
	for name, value := range request.Header {
		newName := strings.ReplaceAll(strings.ToUpper(name), "-", "_")
		newHeaders[newName] = value[0]
	}
	host, _, err := net.SplitHostPort(request.RemoteAddr)
	if err == nil {
		newHeaders["REMOTE_ADDR"] = host
	} else {
		u.Logger.Warn(err)
	}
	return newHeaders
}

// Fetch Fetch blob data from upstream
func (u *GRPCUpstream) Fetch(request http.Request) (*p2client.ServeReply, error) {
	sessionCookie, err := request.Cookie("sessionid")
	// Session is only optional, so we ignore errors here
	session := ""
	if err != nil {
		u.Logger.Debug(err)
	} else {
		session = sessionCookie.Value
	}
	grpcRequest := &p2client.ServeRequest{
		Headers: u.headersToDjango(request),
		Session: session,
		Url:     request.URL.String()}
	response, err := u.ServeClient.RetrieveFile(context.Background(), grpcRequest)
	if err != nil {
		return nil, err
	}
	return response, nil
}
