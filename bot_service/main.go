package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/bwmarrin/discordgo"
)

var rankingMode bool
var votesOne int
var votesTwo int

func main() {
	votesOne = 0
	votesTwo = 0
	rankingMode = false
	// token := os.Getenv("DISCORD_BOT_TOKEN")
	token := "NzYzOTE5MzIxNjEyNDE5MTMz.Gze6CI.Fcgp47xMbnRhzD4Cf3oYV4Dnn5jvdX8cVSrKu0"
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
	fmt.Printf("Message: %s.\n", message)

	if len(message) < 9 {
		return
	} else {
		if message[:9] == "!kukebot " {
			if message[9:] == "ranking" {
				rankingMode = true
				s.ChannelMessageSend(m.ChannelID, "Ranking mode enabled")
				go doRanking(s, m.ChannelID)
			} else {
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

func doRanking(s *discordgo.Session, ChannelID string) {
	arr := []int{9, 5, 1, 3, 8, 4, 2, 7, 6}
	n := len(arr)

	temp := make([]int, n)
	copy(temp, arr)

	for currSize := 1; currSize < n; currSize *= 2 {
		for leftStart := 0; leftStart < n-1; leftStart += 2 * currSize {
			mid := min(leftStart+currSize-1, n-1)
			rightEnd := min(leftStart+2*currSize-1, n-1)

			merge(temp, leftStart, mid, rightEnd, s, ChannelID)
		}
	}

	strSlice := make([]string, len(temp))
	for i, num := range temp {
		strSlice[i] = strconv.Itoa(num)
	}

	result := strings.Join(strSlice, ", ")
	s.ChannelMessageSend(ChannelID, result)
	rankingMode = false
	return
}

func merge(arr []int, leftStart, mid, rightEnd int, s *discordgo.Session, ChannelID string) {
	leftSize := mid - leftStart + 1
	rightSize := rightEnd - mid

	left := make([]int, leftSize)
	right := make([]int, rightSize)

	for i := 0; i < leftSize; i++ {
		left[i] = arr[leftStart+i]
	}

	for j := 0; j < rightSize; j++ {
		right[j] = arr[mid+1+j]
	}

	i, j, k := 0, 0, leftStart

	for i < leftSize && j < rightSize {
		votesOne = 0
		votesTwo = 0
		s.ChannelMessageSend(ChannelID, strconv.Itoa(left[i]))
		s.ChannelMessageSend(ChannelID, strconv.Itoa(right[j]))
		time.Sleep(6 * time.Second)
		if votesOne <= votesTwo {
			arr[k] = left[i]
			i++
		} else {
			arr[k] = right[j]
			j++
		}
		k++
	}

	for i < leftSize {
		arr[k] = left[i]
		i++
		k++
	}

	for j < rightSize {
		arr[k] = right[j]
		j++
		k++
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
