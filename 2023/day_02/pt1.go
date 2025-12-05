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
	cubeMax := map[string]int{"r": 12, "g": 13, "b": 14}

	for i, line := range lines {
		line = line[strings.Index(line, ":")+1:]
		possible := true

		r := regexp.MustCompile(`(\d+)\s(r|g|b)`)
		matches := r.FindAllStringSubmatch(line, -1)

		for _, match := range matches {
			count, _ := strconv.Atoi(match[1])
			if count > cubeMax[match[2]] {
				possible = false
				break
			}
		}

		if possible {
			score += i
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

	helper.CopyClipboard(strconv.Itoa(output))
}
