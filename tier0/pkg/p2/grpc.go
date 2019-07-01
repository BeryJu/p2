package p2

import (
	"context"
	"net/http"

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

// Fetch Fetch blob data from upstream
func (u *GRPCUpstream) Fetch(request http.Request) (*p2client.ServeReply, error) {
	headers := make(map[string]string, 0)
	for name, value := range request.Header {
		headers[name] = value[0]
	}
	sessionCookie, err := request.Cookie("sessionid")
	session := ""
	if err == nil {
		session = sessionCookie.Value
	}
	response, err := u.ServeClient.RetrieveFile(context.Background(), &p2client.ServeRequest{
		Headers: headers,
		Session: session,
		Url:     request.URL.String()})
	if err != nil {
		u.Logger.Error(err)
	}
	return response, nil
}
