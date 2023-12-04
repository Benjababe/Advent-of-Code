package main

import (
	"fmt"
	"strconv"

	"github.com/benjababe/advent-of-code/helper"
)

func solve(lines []string) int64 {
	score := int64(0)

	for _, line := range lines {
		helper.Unused(line)
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

	helper.CopyClipboard(strconv.FormatInt(output, 10))
}
