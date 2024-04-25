package main

import (
	"log"

	"github.com/caarlos0/env/v11"
)

type Config struct {
	DiscordBotToken string
	LLMBackendHost  string `envDefault:"localhost"`
	LLMBackendPort  string `envDefault:"8000"`
}

var AppConfig *Config

func loadEnv() {
	AppConfig = &Config{}
	opts := env.Options{UseFieldNameByDefault: true, RequiredIfNoDef: true}

	if err := env.ParseWithOptions(AppConfig, opts); err != nil {
		log.Fatal(err)
	}
}
