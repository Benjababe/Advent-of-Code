package day02

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func solvePt1(lines []string) int {
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

func Pt1() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt1(lines)
	fmt.Printf("Day 2\tPt1:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
