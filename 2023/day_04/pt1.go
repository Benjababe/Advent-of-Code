package day04

import (
	"fmt"
	"regexp"
	"slices"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func solvePt1(lines []string) int64 {
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

func Pt1() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt1(lines)
	fmt.Printf("Day 4\tPt1:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
