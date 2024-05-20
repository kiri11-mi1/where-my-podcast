package main

import (
	"log"

	"github.com/caarlos0/env/v6"
)

type Config struct {
	TelegramToken string `env:"TELEGRAM_TOKEN"`
}

var cfg Config

func GetVal() Config {
	if err := env.Parse(&cfg); err != nil {
		log.Fatalln("Config", err)
	}
	return cfg
}
