package main

import (
	"fmt"

	"github.com/benjababe/advent-of-code/helper"
)

func solve(lines []string) int {
	return 0
}

func main() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solve(lines)
	fmt.Printf("Output: %d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
