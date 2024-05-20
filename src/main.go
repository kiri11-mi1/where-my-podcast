package main

import (
	"log"
	"time"

	tg "gopkg.in/telebot.v3"
)

func main() {
	pref := tg.Settings{
		Token:  GetVal().TelegramToken,
		Poller: &tg.LongPoller{Timeout: 10 * time.Second},
	}
	b, err := tg.NewBot(pref)
	if err != nil {
		log.Fatal(err)
		return
	}

	// b.Handle("/start", handlerManager.HandleVPN)

	log.Println(b.Me.Username, "start working...")
	b.Start()
}
