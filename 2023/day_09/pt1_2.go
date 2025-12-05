package main

import (
	"fmt"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func isZero(v int64) bool {
	return v == 0
}

func iterPredictions(preds []int64) (int64, int64) {
	if helper.SlicesAll[int64](preds, isZero) {
		return 0, 0
	}

	diffs := []int64{}
	for i := range preds {
		if i == 0 {
			continue
		}

		diffs = append(diffs, preds[i]-preds[i-1])
	}

	next1, next2 := iterPredictions(diffs)
	return preds[len(preds)-1] + next1, preds[0] - next2
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	for _, line := range lines {
		preds, _ := helper.SliceStrToInt64(strings.Split(line, " "))
		v1, v2 := iterPredictions(preds)
		p1 += v1
		p2 += v2
	}

	return p1, p2
}

func main() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Silver: %d\nGold: %d\n", p1, p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
