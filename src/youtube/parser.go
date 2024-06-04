package youtube

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"

	"math"

	"github.com/PuerkitoBio/goquery"
)

type Parser struct{}
type Video struct {
	Id        string
	Title     string
	Channel   string
	Duration  int
	Thumbnail string
}

func NewParser() *Parser {
	return &Parser{}
}

func (p *Parser) Id2Video(id string) (Video, error) {
	link := fmt.Sprintf("https://www.youtube.com/watch?v=%s", id)
	resp, err := http.Get(link)
	if err != nil {
		log.Println("error fetching video info", err)
		return Video{}, ErrFetchingVideoInfoFailed
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		log.Println("error fetching video info", resp.StatusCode)
		return Video{}, ErrFetchingVideoInfoFailed
	}
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Println("error read body:", err)
		return Video{}, err
	}
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(body)))
	if err != nil {
		log.Println("error parse html:", err)
		return Video{}, ErrParseHTMLFailed
	}
	v := Video{Id: id, Title: p.parseTitle(doc), Channel: p.parseChannel(doc), Duration: p.parseDuration(doc), Thumbnail: p.parseThumbnail(doc)}
	return v, nil
}

func (p *Parser) parseTitle(doc *goquery.Document) string {
	title := doc.Find("meta[name='title']").AttrOr("content", "")
	if title == "" {
		log.Println("title not found")
		return ""
	}
	return title
}

func (p *Parser) parseDuration(doc *goquery.Document) int {
	duration := doc.Find("#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div.ytp-time-display.notranslate > span:nth-child(2) > span.ytp-time-duration").Text()
	if duration == "" {
		log.Println("duration not found")
		return 0
	}
	parts := strings.Split(duration, ":")
	seconds := 0
	counter := 0
	for i := len(parts) - 1; i >= 0; i-- {
		num, _ := strconv.Atoi(parts[i])
		seconds += num * int(math.Pow(60, float64(counter)))
		counter++
	}

	return seconds
}

func (p *Parser) parseChannel(doc *goquery.Document) string {
	channelName := doc.Find("a.yt-simple-endpoint.style-scope.yt-formatted-string").First().Text()
	if channelName == "" {
		log.Println("chanel not found")
		return ""
	}
	return channelName
}

func (p *Parser) parseThumbnail(doc *goquery.Document) string {
	pic := doc.Find("link[itemprop='thumbnailUrl']").AttrOr("href", "")
	if pic == "" {
		log.Println("thumbnail not found")
		return ""
	}
	return pic
}
