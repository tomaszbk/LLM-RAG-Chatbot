package main

import (
	"fmt"
	"testing"
)

func TestLlmPostRequest(t *testing.T) {
	prompt := "Hello"
	reply, err := LlmPostRequest(prompt)
	if err != nil {
		t.Errorf("Error: %v", err)
	}
	fmt.Printf("Reply: %s\n", reply)
}
