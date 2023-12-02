package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func solve(lines []string) int {
	score := 0
	cubeMax := []int{12, 13, 14}

	for i, line := range lines {
		line = line[strings.Index(line, ":")+1:]
		possible := true
		patterns := []string{`(\d+)\sred`, `(\d+)\sgreen`, `(\d+)\sblue`}

		for colIndex, pattern := range patterns {
			regex := regexp.MustCompile(pattern)
			matches := regex.FindAllStringSubmatch(line, -1)

			for _, match := range matches {
				count, _ := strconv.Atoi(match[1])
				if count > cubeMax[colIndex] {
					possible = false
				}
			}
		}

		if possible {
			score += i + 1
		}
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
}
