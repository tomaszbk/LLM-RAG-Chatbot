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

func main() {

	// token := os.Getenv("DISCORD_BOT_TOKEN")
	token := "NzYzOTE5MzIxNjEyNDE5MTMz.GG7F12.4AinvOKnAvC55TgxGMWe1K81bHzqzksNVVgSe8"
	if token == "" {
		fmt.Println("Bot token not provided. Please set the DISCORD_BOT_TOKEN environment variable.")
		return
	}

	ds_bot, err := discordgo.New("Bot " + token)
	if err != nil {
		fmt.Println("Error creating Discord session:", err)
		return
	}

	ds_bot.AddHandler(messageCreate)

	ds_bot.Identify.Intents = discordgo.IntentsAllWithoutPrivileged

	// Open a connection to Discord
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

func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {
	// Ignore messages from the bot itself
	if m.Author.ID == s.State.User.ID {
		return
	}

	fmt.Printf("[%s] (Channel: %s) %s: %s\n", m.GuildID, m.ChannelID, m.Author.Username, m.Content)
	message := m.Content
	if len(message) < 9 {
		return
	}
	fmt.Printf("Message: %s.\n", message[:9])
	if message[:9] == "!kukebot " {
		fmt.Println("Processing prompt")
		croppedMessage := message[9:]
		promptAnswer, err := LlmPostRequest(croppedMessage)
		if err != nil {
			fmt.Println("Error processing prompt: ", err)
		} else {
			s.ChannelMessageSend(m.ChannelID, promptAnswer)
		}

	}
}

func LlmPostRequest(prompt string) (string, error) {
	// jsonData, err := json.Marshal(map[string]string{"prompt": prompt})
	jsonData, err := json.Marshal(map[string]string{"prompt": prompt})

	if err != nil {
		return "", err
	}

	// err = os.WriteFile("output.json", jsonData, 0644)

	if err != nil {
		return "", err
	}

	resp, err := http.Post("http://localhost:8000/submit_prompt", "application/json", bytes.NewBuffer(jsonData))
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

	return string(content), nil
}

// // Unmarshal the JSON response
// var responseMap map[string]interface{}
// err = json.Unmarshal(body, &responseMap)
// if err != nil {
// 	fmt.Println("Error unmarshaling JSON:", err)
// 	return
// }

// // Print the JSON response
// fmt.Println("JSON Response:", responseMap)
