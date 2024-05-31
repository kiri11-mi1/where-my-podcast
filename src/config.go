package main

import (
	"log"

	"github.com/caarlos0/env/v6"
)

type Config struct {
	TelegramToken string `env:"TELEGRAM_TOKEN"`
	RedisUrl      string `env:"REDIS_URL"`
}

var cfg Config

func GetEnv() Config {
	if err := env.Parse(&cfg); err != nil {
		log.Fatalln("Config", err)
	}
	return cfg
}
