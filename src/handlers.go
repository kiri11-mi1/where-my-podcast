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

type Handler struct {
	cache   Cache
	service YoutubeService
}

func NewHandler(cache Cache, service YoutubeService) *Handler {
	return &Handler{
		cache:   cache,
		service: service,
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
	fileId := h.cache.Get(ytId)
	if fileId == PENDING {
		_, err := c.Bot().Send(c.Recipient(), "Wait...")
		return err
	}
	if fileId != "" {
		log.Println("get audio from cache")
		audio := &tg.Audio{File: tg.File{FileID: fileId}}
		_, err = c.Bot().Send(c.Recipient(), audio)
		return err
	}
	h.cache.Set(ytId, PENDING)
	log.Println("downloading", link)
	filePath, err := h.service.Download(link, ytId)
	defer os.Remove(filePath)
	if err != nil {
		log.Println(err)
		h.cache.Set(ytId, "")
		_, err = c.Bot().Send(c.Recipient(), "error downloading audio")
		return err
	}
	audio := &tg.Audio{File: tg.FromDisk(filePath)}
	h.cache.Set(ytId, audio.FileID)
	_, err = c.Bot().Send(c.Recipient(), audio)
	return err
}
