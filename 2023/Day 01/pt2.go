package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func replaceNumText(numMap map[string]string, line string) string {
	for true {
		done := true
		for numText, num := range numMap {
			if strings.Contains(line, numText) {
				line = strings.ReplaceAll(line, numText, num)
				done = false
			}
		}

		if done {
			break
		}
	}
	return line
}

func solve(lines []string) int {
	score := 0

	numMap := map[string]string{
		"one": "o1e", "two": "t2o", "three": "t3e",
		"four": "f4r", "five": "f5e", "six": "s6e",
		"seven": "s7n", "eight": "e8t", "nine": "n9e",
	}

	for _, line := range lines {
		start, last := 0, 0
		line = replaceNumText(numMap, line)

		for i := 0; i < len(line); i++ {
			char := line[i]
			if '0' <= char && char <= '9' {
				if start == 0 {
					start = int(char - '0')
				}
				last = int(char - '0')
			}
		}

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

	helper.CopyClipboard(strconv.Itoa(output))
}
