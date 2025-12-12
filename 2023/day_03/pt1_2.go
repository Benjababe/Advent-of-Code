package day03

import (
	"fmt"
	"regexp"
	"slices"
	"strconv"

	"github.com/benjababe/advent-of-code/helper"
)

type Cell struct {
	Value int64
	ID    int64
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
				grid[i][j] = Cell{Value: num, ID: idCount}
			}
			idCount++
		}
	}
}

func getNumsAdjacent(grid [][]Cell, i int, j int) []int64 {
	nums := []int64{}
	numIDs := []int64{}

	for _i := -1; _i <= 1; _i++ {
		for _j := -1; _j <= 1; _j++ {
			di, dj := i+_i, j+_j
			if di < 0 || di >= len(grid) || dj < 0 || dj >= len(grid[di]) {
				continue
			}

			cell := grid[di][dj]
			if cell.ID > 0 && !slices.Contains(numIDs, cell.ID) {
				nums = append(nums, cell.Value)
				numIDs = append(numIDs, cell.ID)
			}
		}
	}

	return nums
}

func searchGrid(grid [][]Cell, lines []string, pt2 bool) int64 {
	score := int64(0)

	for i, row := range lines {
		for j, char := range row {
			if !pt2 {
				if isSymbol(char) {
					for _, num := range getNumsAdjacent(grid, i, j) {
						score += num
					}
				}
			} else {
				if char == '*' {
					nums := getNumsAdjacent(grid, i, j)
					if len(nums) == 2 {
						score += nums[0] * nums[1]
					}
				}
			}
		}
	}

	return score
}

func solve(lines []string, pt2 bool) int64 {
	grid := make([][]Cell, len(lines))
	populateGrid(grid, lines)
	return searchGrid(grid, lines, pt2)
}

func Pt1() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solve(lines, false)
	fmt.Printf("Day 3\tPt1:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}

func Pt2() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solve(lines, true)
	fmt.Printf("Day 3\tPt2:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
