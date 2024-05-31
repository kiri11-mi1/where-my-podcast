package youtube

import (
	"net/url"
	"regexp"
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

	return false
}

func Link2Id(url string) (string, error) {
	// Fetching video id from youtube url
	return "id", nil
}
