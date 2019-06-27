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
	URL string
}

// Blob Hold information about Blob
type Blob struct {
	Data     []byte
	MimeType string
	ModTime  time.Time
}

// Fetch Fetch Blob from upstream p2 server
func (u *Upstream) Fetch(key string) (Blob, error) {
	realKey, err := url.QueryUnescape(key)
	resp, err := http.Get(u.URL + realKey)
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
