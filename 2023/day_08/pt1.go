package day08

import (
	"fmt"
	"regexp"

	"github.com/benjababe/advent-of-code/helper"
)

func solvePt1(lines []string) int64 {
	score := int64(0)

	instructions := lines[0]
	nodeMap := make(map[string](map[rune]string))
	nodeRegex := regexp.MustCompile(`(\w+)\s=\s\((\w+),\s(\w+)\)`)

	for _, line := range lines[1:] {
		if len(line) == 0 {
			continue
		}

		match := nodeRegex.FindStringSubmatch(line)
		src, l, r := match[1], match[2], match[3]
		nodeMap[src] = map[rune]string{'L': l, 'R': r}

		helper.Unused(line, match)
	}

	curNode := "AAA"
	for curNode != "ZZZ" {
		for _, inst := range instructions {
			curNode = nodeMap[curNode][inst]
			score++
		}
	}

	return score
}

func Pt1() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt1(lines)
	fmt.Printf("Day 8\tPt1:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
