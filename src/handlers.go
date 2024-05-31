package main

import (
	"where-my-podcast/youtube"

	tg "gopkg.in/telebot.v3"
)

type Cache interface {
	Get(id string) string                // TODO: может быть int64
	Set(youtubeId string, fileId string) //TODO: fileId может быть int64
}

type YoutubeService interface {
	// TODO: добавить методы для работы с youtube
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
	if !youtube.IsValidLink(c.Message().Text) {
		_, err := c.Bot().Send(c.Recipient(), "Ссылка неверна")
		return err
	}
	ytId, err := youtube.Link2Id(c.Message().Text)
	if err != nil {
		// TODO: добавить логгирование
		return err
	}
	// fileId := h.cache.Get(ytId)
	// if fileId == "" {
	// 	// TODO: скачивание ролика
	// 	// path := h.service.Download()
	// 	// audio := &tg.Audio{File: tg.FromDisk(filePath)}

	// 	// TODO: сохранение fileId в бд
	// 	// h.cache.Set(ytId, fileId)
	// } else {
	// 	// audio := &tg.Audio{File: tg.File{FileID: fileId}}
	// 	// c.Bot().Send(c.Recipient(), audio)
	// }
	_, err = c.Bot().Send(c.Recipient(), ytId)
	return err
}
