package day15

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

var boxes [][]string

func hash(step string) int64 {
	value := int64(0)
	for _, char := range step {
		value += int64(char)
		value *= 17
		value %= 256
	}
	return value
}

func hashmap(step string) {
	if step[len(step)-1] == '-' {
		label := step[:len(step)-1]
		boxIndex := hash(label)
		boxes[boxIndex] = helper.SliceFilter[string](boxes[boxIndex], func(s string) bool {
			return !strings.Contains(s, label)
		})
	} else {
		label := strings.Split(step, "=")[0]
		boxIndex := hash(label)
		for i, lens := range boxes[boxIndex] {
			if strings.Contains(lens, label) {
				boxes[boxIndex][i] = step
				return
			}
		}
		boxes[boxIndex] = append(boxes[boxIndex], step)
	}
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	steps := strings.Split(lines[0], ",")

	boxes = [][]string{}
	for i := 0; i < 256; i++ {
		boxes = append(boxes, []string{})
	}

	for _, step := range steps {
		p1 += hash(step)
		hashmap(step)
	}

	for i, box := range boxes {
		for j, lens := range box {
			focalLen, _ := strconv.ParseInt(strings.Split(lens, "=")[1], 10, 64)
			p2 += int64(i+1) * int64(j+1) * focalLen
		}
	}

	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 15\tPt1:\t%d\n", p1)
	fmt.Printf("Day 15\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
