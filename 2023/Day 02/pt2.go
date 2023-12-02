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

	for _, line := range lines {
		line = line[strings.Index(line, ":")+1:]
		minCubes := map[string]int{"r": 0, "g": 0, "b": 0}

		r := regexp.MustCompile(`(\d+)\s(r|g|b)`)
		matches := r.FindAllStringSubmatch(line, -1)

		for _, match := range matches {
			count, _ := strconv.Atoi(match[1])
			if count > minCubes[match[2]] {
				minCubes[match[2]] = count
			}
		}

		score += minCubes["r"] * minCubes["g"] * minCubes["b"]
	}

	return score
}

func main() {
	lines := []string{}
	helper.GetLines(&lines, "bigboy03.txt")

	start := helper.GetCurrentTime()
	output := solve(lines)
	fmt.Printf("Output: %d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)

	helper.CopyClipboard(strconv.Itoa(output))
}
