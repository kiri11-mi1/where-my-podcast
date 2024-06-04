package main

import (
	yt "where-my-podcast/youtube"

	tg "gopkg.in/telebot.v3"
)

func MakeAudio(v yt.Video, fileStr string) *tg.Audio {
	file := tg.FromDisk(fileStr)
	thumbnail := &tg.Photo{File: tg.FromURL(v.Thumbnail)}
	return &tg.Audio{File: file, Performer: v.Channel, Title: v.Title, Thumbnail: thumbnail, Duration: v.Duration}
}
