package day08

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func gcd(a, b int64) int64 {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func lcm(nums []int64) int64 {
	if len(nums) == 0 {
		panic("No numbers to lcm")
	} else if len(nums) == 1 {
		return nums[0]
	}

	res := nums[0] * nums[1] / gcd(nums[0], nums[1])

	for _, num := range nums[2:] {
		res = lcm([]int64{res, num})
	}

	return res
}

func solvePt2(lines []string) int64 {
	score := int64(0)
	steps := int64(0)

	curNodes := []string{}
	minSteps := []int64{}
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

		if strings.HasSuffix(src, "A") {
			curNodes = append(curNodes, src)
			minSteps = append(minSteps, int64(0))
		}
	}

	for helper.SlicesAny(minSteps, func(steps int64) bool { return steps == 0 }) {
		for _, inst := range instructions {
			steps++

			for i, node := range curNodes {
				curNodes[i] = nodeMap[node][inst]

				if strings.HasSuffix(curNodes[i], "Z") && minSteps[i] == 0 {
					minSteps[i] = steps
				}
			}
		}
	}

	score = lcm(minSteps[0:2])
	return score
}

func Pt2() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt2(lines)
	fmt.Printf("Day 8\tPt2:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
