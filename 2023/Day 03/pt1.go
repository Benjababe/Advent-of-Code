package main

import (
	"fmt"
	"regexp"
	"slices"
	"strconv"

	"github.com/benjababe/advent-of-code/helper"
)

type Cell struct {
	Value int64
	Id    int64
}

func isSymbol(char rune) bool {
	return !(char == '.' || ('0' <= char && char <= '9'))
}

func populateGrid(grid [][]Cell, lines []string) {
	regex := regexp.MustCompile(`(\d+)`)
	idCount := int64(1)

	for i, line := range lines {
		grid[i] = make([]Cell, len(line))
		matches := regex.FindAllStringIndex(line, -1)

		for _, match := range matches {
			numStr := line[match[0]:match[1]]
			for j := match[0]; j < match[1]; j++ {
				num, _ := strconv.ParseInt(numStr, 10, 64)
				grid[i][j] = Cell{Value: num, Id: idCount}
			}
			idCount++
		}
	}
}

func getNumsAdjacent(grid [][]Cell, i int, j int) []int64 {
	nums := []int64{}
	numIds := []int64{}

	for _i := -1; _i <= 1; _i++ {
		for _j := -1; _j <= 1; _j++ {
			di, dj := i+_i, j+_j

			if di < 0 || di >= len(grid) || dj < 0 || dj >= len(grid[di]) {
				continue
			}

			cell := grid[di][dj]
			if cell.Id > 0 && !slices.Contains(numIds, cell.Id) {
				nums = append(nums, cell.Value)
				numIds = append(numIds, cell.Id)
			}
		}
	}

	return nums
}

func searchGrid(grid [][]Cell, lines []string) int64 {
	score := int64(0)

	for i, row := range lines {
		for j, char := range row {
			if isSymbol(char) {
				for _, num := range getNumsAdjacent(grid, i, j) {
					score += num
				}
			}
		}
	}

	return score
}

func solve(lines []string) int64 {
	grid := make([][]Cell, len(lines))
	populateGrid(grid, lines)
	return searchGrid(grid, lines)
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
