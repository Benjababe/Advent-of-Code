package main

import (
	"fmt"
	"regexp"
	"slices"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func solve(lines []string) int64 {
	score := int64(0)

	for _, line := range lines {
		points := int64(0)

		regex := regexp.MustCompile(`^.+\:(.*)\|(.*)$`)
		matches := regex.FindStringSubmatch(line)
		winners, has := matches[1], matches[2]

		winnerSlice := strings.Split(strings.TrimSpace(winners), " ")
		hasSlice := strings.Split(strings.TrimSpace(has), " ")

		for _, number := range hasSlice {
			number = strings.TrimSpace(number)
			if slices.Contains(winnerSlice, number) && number != "" {
				if points == 0 {
					points = 1
				} else {
					points *= 2
				}
			}
		}

		score += points
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

	helper.CopyClipboard(strconv.FormatInt(output, 10))
}
