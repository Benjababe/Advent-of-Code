package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func findFirst(numMap map[string]string, line string) int {
	for len(line) > 0 {
		for num := int64(1); num < 10; num++ {
			if string(line[0]) == strconv.FormatInt(num, 10) {
				return int(num)
			}
		}

		for numText, num := range numMap {
			if strings.HasPrefix(line, numText) {
				i, _ := strconv.Atoi(num)
				return i
			}
		}

		line = line[1:]
	}

	return -1
}

func findLast(numMap map[string]string, line string) int {
	for len(line) > 0 {
		lastI := len(line) - 1

		for num := int64(1); num < 10; num++ {
			if string(line[lastI]) == strconv.FormatInt(num, 10) {
				return int(num)
			}
		}

		for numText, num := range numMap {
			if strings.HasSuffix(line, numText) {
				i, _ := strconv.Atoi(num)
				return i
			}
		}

		line = line[:lastI]
	}

	return -1
}

func solve(lines []string) int {
	score := 0

	numMap := map[string]string{
		"one": "1", "two": "2", "three": "3",
		"four": "4", "five": "5", "six": "6",
		"seven": "7", "eight": "8", "nine": "9",
	}

	for _, line := range lines {
		first := findFirst(numMap, line)
		last := findLast(numMap, line)
		score += first*10 + last
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
