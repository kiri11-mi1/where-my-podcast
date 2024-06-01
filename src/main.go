package main

import (
	"log"
	"time"
	"where-my-podcast/storage"
	"where-my-podcast/youtube"

	tg "gopkg.in/telebot.v3"
)

func main() {
	pref := tg.Settings{
		Token:  GetEnv().TelegramToken,
		Poller: &tg.LongPoller{Timeout: 10 * time.Second},
	}
	b, err := tg.NewBot(pref)
	if err != nil {
		log.Fatal(err)
		return
	}

	cache := storage.NewCache(GetEnv().RedisUrl, 2000*time.Hour)
	ytService := youtube.NewDownloader("./downloads")
	handler := NewHandler(cache, ytService)
	b.Handle("/start", handler.HandleStart)
	b.Handle(tg.OnText, handler.HandleMessage)

	log.Println(b.Me.Username, "start working...")
	b.Start()
}
