package main

import (
	"log"
	"os"
	"where-my-podcast/youtube"

	tg "gopkg.in/telebot.v3"
)

const PENDING string = "pending"

type Cache interface {
	Get(id string) string
	Set(youtubeId string, fileId string) error
}

type YoutubeService interface {
	Download(link, videoId string) (string, error)
}

type Parser interface {
	Id2Video(id string) (youtube.Video, error)
}

type Handler struct {
	cache   Cache
	service YoutubeService
	parser  Parser
}

func NewHandler(cache Cache, service YoutubeService, parser Parser) *Handler {
	return &Handler{
		cache:   cache,
		service: service,
		parser:  parser,
	}
}

func (h *Handler) HandleStart(c tg.Context) error {
	_, err := c.Bot().Send(c.Recipient(), "Hi, copy and paste youtube url and get audio file!")
	return err
}

func (h *Handler) HandleMessage(c tg.Context) error {
	link := c.Message().Text
	ytId, err := youtube.Link2Id(c.Message().Text)
	if err != nil {
		log.Println(err)
		_, err := c.Bot().Send(c.Recipient(), "Check youtube url")
		return err
	}
	video, err := h.parser.Id2Video(ytId)
	if err != nil {
		log.Println(err)
		_, err := c.Bot().Send(c.Recipient(), "error fetching video info")
		return err
	}
	fileId := h.cache.Get(ytId)
	if fileId == PENDING {
		_, err := c.Bot().Send(c.Recipient(), "Wait...")
		return err
	}
	if fileId != "" {
		log.Println("get audio from cache")
		audio := MakeAudio(video, fileId, false)
		_, err = c.Bot().Send(c.Recipient(), audio)
		return err
	}
	h.cache.Set(ytId, PENDING)
	log.Println("downloading...", link)
	filePath, err := h.service.Download(link, ytId)
	defer os.Remove(filePath)
	if err != nil {
		log.Println(err)
		h.cache.Set(ytId, "")
		_, err = c.Bot().Send(c.Recipient(), "error downloading audio")
		return err
	}
	log.Println("video: ", video.Id, video.Channel, video.Title, video.Duration)
	audio := MakeAudio(video, filePath, true)
	_, err = c.Bot().Send(c.Recipient(), audio)
	h.cache.Set(ytId, audio.FileID)
	return err
}
