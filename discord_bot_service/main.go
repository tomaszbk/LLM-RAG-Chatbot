package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
)

var rankingMode bool
var votesOne int
var votesTwo int

func main() {
	rankingMode = false
	loadEnv()
	if AppConfig.DiscordBotToken == "" {
		fmt.Println("Bot token not provided. Please set the DISCORD_BOT_TOKEN environment variable.")
		return
	}

	ds_bot, err := discordgo.New("Bot " + AppConfig.DiscordBotToken)
	if err != nil {
		fmt.Println("Error creating Discord session:", err)
		return
	}

	ds_bot.AddHandler(OnMessageCreate)

	ds_bot.Identify.Intents = discordgo.IntentsAllWithoutPrivileged

	err = ds_bot.Open()
	if err != nil {
		fmt.Println("Error opening connection to Discord:", err)
		return
	}

	fmt.Println("Bot is now running. Press Ctrl+C to exit.")

	// Wait for a termination signal to gracefully shut down the bot
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
	ds_bot.Close()
}

func OnMessageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {
	// Ignore messages from the bot itself
	if m.Author.ID == s.State.User.ID {
		return
	}

	if rankingMode {
		if m.Content == "1" {
			votesOne++
			return
		} else if m.Content == "2" {
			votesTwo++
			return
		}
	}

	fmt.Printf("[%s] (Channel: %s) %s: %s\n", m.GuildID, m.ChannelID, m.Author.Username, m.Content)
	message := m.Content

	if len(message) < 4 {
		return
	}

	if message[:4] == "!kb " {
		if message[3:] == "ranking" {
			go doRanking(s, m.ChannelID)
		} else {
			go GetLlmResponse(s, m, message[4:])
		}
	}
}

func GetLlmResponse(s *discordgo.Session, m *discordgo.MessageCreate, prompt string) {
	fmt.Println("Processing prompt")
	croppedMessage := fmt.Sprintf("soy %s, %s", m.Author.Username, prompt)
	promptAnswer, err := LlmPostRequest(croppedMessage)
	if err != nil {
		fmt.Println("Error processing prompt: ", err)
		s.ChannelMessageSend(m.ChannelID, "Error...")
	} else {
		s.ChannelMessageSend(m.ChannelID, promptAnswer)
	}
}

type LlmPayload struct {
	Prompt string `json:"prompt"`
}

func LlmPostRequest(prompt string) (string, error) {
	payload := &LlmPayload{Prompt: prompt}
	jsonData, err := json.Marshal(payload)

	if err != nil {
		return "", err
	}
	url := fmt.Sprintf("http://%s:%s/submit-prompt", AppConfig.LLMBackendHost, AppConfig.LLMBackendPort)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("POST request failed with status code: %d", resp.StatusCode)
	}

	content, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	var r string
	err = json.Unmarshal(content, &r)
	if err != nil {
		return "", err
	}

	return r, nil
}
