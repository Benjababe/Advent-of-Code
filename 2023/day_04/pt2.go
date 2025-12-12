package day04

import (
	"fmt"
	"regexp"
	"slices"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func solvePt2(lines []string) int64 {
	score := int64(0)
	cardCount := make(map[int]int64)

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
				winCount++
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

func Pt2() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt2(lines)
	fmt.Printf("Day 4\tPt2:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
