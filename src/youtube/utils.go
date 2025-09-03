package youtube

import (
	"net/url"
	"regexp"
	"strings"
)

func IsValidLink(link string) bool {
	// Checking if youtube url is valid
	parsedURL, err := url.Parse(link)
	if err != nil {
		return false
	}

	if parsedURL.Host != "www.youtube.com" && parsedURL.Host != "youtube.com" && parsedURL.Host != "youtu.be" {
		return false
	}

	if parsedURL.Host == "youtu.be" {
		match, _ := regexp.MatchString(`^[a-zA-Z0-9_-]{11}$`, parsedURL.Path[1:])
		return match
	}

	if parsedURL.Path == "/watch" {
		queryParams := parsedURL.Query()
		if val, ok := queryParams["v"]; ok {
			match, _ := regexp.MatchString(`^[a-zA-Z0-9_-]{11}$`, val[0])
			return match
		}
	}

	if strings.HasPrefix(parsedURL.Path, "/shorts/") {
		id := strings.TrimPrefix(parsedURL.Path, "/shorts/")
		match, _ := regexp.MatchString(`^[a-zA-Z0-9_-]{11}$`, id)
		return match
	}

	return false
}

func Link2Id(link string) (string, error) {
	// Fetching video id from youtube url
	if !IsValidLink(link) {
		return "", ErrInvalidYoutubeLink
	}

	parsedURL, err := url.Parse(link)
	if err != nil {
		return "", err
	}
	var id string
	switch {
	case parsedURL.Host == "youtu.be":
		id = parsedURL.Path[1:]
	case parsedURL.Path == "/watch":
		queryParams := parsedURL.Query()
		id = queryParams.Get("v")
	case strings.HasPrefix(parsedURL.Path, "/shorts/"):
		id = strings.TrimPrefix(parsedURL.Path, "/shorts/")
	}

	return id, nil
}
