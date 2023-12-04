package main

import (
	"fmt"
	"regexp"
	"slices"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func solve(lines []string) int {
	score := 0
	cardCount := make(map[int]int)

	for i, line := range lines {
		if cardCount[i] == 0 {
			cardCount[i] = 1
		}

		regex := regexp.MustCompile(`^.+\:(.*)\|(.*)$`)
		matches := regex.FindStringSubmatch(line)
		winners, has := matches[1], matches[2]
		winCount := 0

		winnerSlice := strings.Split(strings.TrimSpace(winners), " ")
		hasSlice := strings.Split(strings.TrimSpace(has), " ")

		for _, number := range hasSlice {
			number = strings.TrimSpace(number)
			if slices.Contains(winnerSlice, number) && number != "" {
				winCount += 1
			}
		}

		for j := 1; j <= winCount; j++ {
			key := i + j
			if cardCount[key] == 0 {
				cardCount[key] = 1
			}

			cardCount[key] += cardCount[i]
		}

		score += cardCount[i]
	}

	return score
}

func main() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solve(lines)
	fmt.Printf("Output: %d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)

	helper.CopyClipboard(strconv.Itoa(output))
}
