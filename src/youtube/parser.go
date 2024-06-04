package youtube

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"

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
	durationStr := doc.Find("meta[itemprop='duration']").AttrOr("content", "")
	if durationStr == "" {
		log.Println("duration not found")
		return 0
	}
	parts := strings.Split(durationStr, "M")
	minutesStr := strings.Replace(parts[0], "PT", "", 1)
	minutes, err := strconv.Atoi(minutesStr)
	if err != nil {
		log.Println("error parse duration:", err)
		return 0
	}
	resultDur := minutes * 60
	secondsStr := strings.Replace(parts[1], "S", "", 1)
	seconds, err := strconv.Atoi(secondsStr)
	if err != nil {
		log.Println("error parse duration:", err)
		return 0
	}
	resultDur += seconds

	return resultDur
}

func (p *Parser) parseChannel(doc *goquery.Document) string {
	channelName := doc.Find("link[itemprop='name']").AttrOr("content", "")
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
