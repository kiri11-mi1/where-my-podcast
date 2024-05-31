package main

import (
	"log"
	"time"
	"where-my-podcast/storage"

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

	cache := storage.NewCache(GetEnv().RedisUrl)
	// ytService = NewYtService(cache)
	handler := NewHandler(cache, nil)
	b.Handle("/start", handler.HandleStart)
	b.Handle(tg.OnText, handler.HandleMessage)

	log.Println(b.Me.Username, "start working...")
	b.Start()
}
