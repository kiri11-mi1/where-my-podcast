package main

import (
	"log"
	"time"

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

	b.Handle(tg.OnText, func(c tg.Context) error {
		_, err := c.Bot().Send(c.Recipient(), "Hello, world!")
		return err
	})

	log.Println(b.Me.Username, "start working...")
	b.Start()
}
