package main

import (
	"fmt"
	"strconv"

	"github.com/benjababe/advent-of-code/helper"
)

func findFirst(line string) int {
	for len(line) > 0 {
		for num := int64(1); num < 10; num++ {
			if string(line[0]) == strconv.FormatInt(num, 10) {
				return int(num)
			}
		}

		line = line[1:]
	}

	return -1
}

func findLast(line string) int {
	for len(line) > 0 {
		lastI := len(line) - 1

		for num := int64(1); num < 10; num++ {
			if string(line[lastI]) == strconv.FormatInt(num, 10) {
				return int(num)
			}
		}

		line = line[:lastI]
	}

	return -1
}

func solve(lines []string) int {
	score := 0

	for _, line := range lines {
		start := findFirst(line)
		last := findLast(line)
		score += start*10 + last
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
