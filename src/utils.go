package main

import (
	tg "gopkg.in/telebot.v3"

	yt "where-my-podcast/youtube"
)

func MakeAudio(v yt.Video, file string, fromDisk bool) *tg.Audio {
	if fromDisk {
		return &tg.Audio{File: tg.FromDisk(file), Performer: v.Channel, Title: v.Title, Duration: v.Duration}
	}
	return &tg.Audio{File: tg.File{FileID: file}, Performer: v.Channel, Title: v.Title, Duration: v.Duration}
}
