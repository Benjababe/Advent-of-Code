package day01

import (
	"fmt"

	"github.com/benjababe/advent-of-code/helper"
)

func solvePt1(lines []string) int {
	score := 0

	for _, line := range lines {
		start, last := 0, 0

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

func Pt1() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt1(lines)
	fmt.Printf("Day 1\tPt1:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
