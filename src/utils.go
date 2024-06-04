package main

import (
	tg "gopkg.in/telebot.v3"

	yt "where-my-podcast/youtube"
)

func MakeAudio(v yt.Video, fileStr string, fromDisk bool) *tg.Audio {
	var file tg.File
	if fromDisk {
		file = tg.FromDisk(fileStr)
	} else {
		file = tg.File{FileID: fileStr}
	}
	return &tg.Audio{File: file, Performer: v.Channel, Title: v.Title, Duration: v.Duration, Thumbnail: &tg.Photo{File: tg.FromURL(v.Thumbnail)}}
}
