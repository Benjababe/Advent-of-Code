package main

import (
	"fmt"

	"github.com/benjababe/advent-of-code/helper"
)

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	for _, line := range lines {
		helper.Unused(line)
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
