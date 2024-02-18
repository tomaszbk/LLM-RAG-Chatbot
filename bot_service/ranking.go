package main

import (
	"strconv"
	"strings"
	"time"

	"github.com/bwmarrin/discordgo"
)

func doRanking(s *discordgo.Session, ChannelID string) {
	arr := []int{9, 7, 6}
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
		s.ChannelMessageSend(ChannelID, "Which is better? "+strconv.Itoa(left[i])+" or "+strconv.Itoa(right[j])+"?")
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
