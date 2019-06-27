package p2

import (
	"errors"
	"io/ioutil"
	"net/http"
	"net/url"
	"time"

	log "github.com/sirupsen/logrus"
)

const rfc2822 = "Mon Jan 02 15:04:05 -0700 2006"

// Upstream Information about the upstream server
type Upstream struct {
	URL    string
	client http.Client
}

// Blob Hold information about Blob
type Blob struct {
	Data     []byte
	MimeType string
	ModTime  time.Time
}

func NewUpstream(URL string) Upstream {
	return Upstream{
		URL: URL,
		client: http.Client{
			CheckRedirect: func(req *http.Request, via []*http.Request) error {
				return http.ErrUseLastResponse
			},
		},
	}
}

// Fetch Fetch Blob from upstream p2 server
func (u *Upstream) Fetch(host string, key string) (Blob, error) {
	// Key is Querystring-escaped to circumvent groupcache bugs
	realKey, err := url.QueryUnescape(key)
	// Build a full request so we can pass the correct Host header
	req, err := http.NewRequest("GET", u.URL+realKey, nil)
	log.Debugf("Patching host to '%s'", host)
	req.Host = host
	resp, err := u.client.Do(req)
	if err != nil {
		return Blob{}, err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return Blob{}, err
	}
	log.Debugf("Response code: %d", resp.StatusCode)
	if body == nil {
		return Blob{}, errors.New("Empty response")
	}
	modTime, err := time.Parse(rfc2822, resp.Header.Get("Last-Modified"))
	if err != nil {
		log.Debug(err)
	}
	return Blob{
		Data:     body,
		MimeType: resp.Header.Get("Content-Type"),
		ModTime:  modTime,
	}, nil
}
