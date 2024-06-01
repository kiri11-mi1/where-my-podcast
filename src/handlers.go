package main

import (
	"log"
	"where-my-podcast/youtube"

	tg "gopkg.in/telebot.v3"
)

type Cache interface {
	GetFileId(id string) string
	SetFileId(youtubeId string, fileId string) error
	SetPending(youtubeId string) error
	IsPending(youtubeId string) bool
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
		_, err := c.Bot().Send(c.Recipient(), "Проверьте ссылку")
		return err
	}
	if h.cache.IsPending(ytId) {
		_, err := c.Bot().Send(c.Recipient(), "Запрос уже обрабатывается")
		return err
	}
	fileId := h.cache.GetFileId(ytId)
	if fileId != "" {
		audio := &tg.Audio{File: tg.File{FileID: fileId}}
		_, err = c.Bot().Send(c.Recipient(), audio)
		return err
	}
	h.cache.SetPending(ytId)
	filePath, err := h.service.Download(link, ytId)
	if err != nil {
		log.Println(err)
		_, err = c.Bot().Send(c.Recipient(), "Произошла ошибка скачивания")
		return err
	}
	audio := &tg.Audio{File: tg.FromDisk(filePath)}
	if err := h.cache.SetFileId(ytId, audio.FileID); err != nil {
		return err
	}
	_, err = c.Bot().Send(c.Recipient(), audio)
	return err
}
