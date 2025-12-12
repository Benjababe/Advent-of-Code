package day10

import (
	"fmt"
	"slices"

	"github.com/benjababe/advent-of-code/helper"
)

type Coord struct {
	x int
	y int
}

type CoordStep struct {
	coord Coord
	step  int64
}

var p1 int64
var p2 int64
var visited map[Coord]int64
var visitedEnclosed map[Coord]int64

func checkPipeConnected(lines []string, x1, y1, x2, y2 int) bool {
	src, dest := lines[y1][x1], lines[y2][x2]

	toWest := []byte{'S', '-', 'J', '7'}
	toEast := []byte{'S', '-', 'F', 'L'}
	toNorth := []byte{'S', '|', 'L', 'J'}
	toSouth := []byte{'S', '|', 'F', '7'}

	fromWest := []byte{'-', 'F', 'L'}
	fromEast := []byte{'-', 'J', '7'}
	fromNorth := []byte{'|', 'F', '7'}
	fromSouth := []byte{'|', 'L', 'J'}

	if x2-x1 == -1 && slices.Contains(toWest, src) && slices.Contains(fromWest, dest) {
		return true
	}

	if x2-x1 == 1 && slices.Contains(toEast, src) && slices.Contains(fromEast, dest) {
		return true
	}

	if y2-y1 == -1 && slices.Contains(toNorth, src) && slices.Contains(fromNorth, dest) {
		return true
	}

	if y2-y1 == 1 && slices.Contains(toSouth, src) && slices.Contains(fromSouth, dest) {
		return true
	}

	return false
}

func findFurthest(lines []string, possible []CoordStep) int64 {
	maxSteps := int64(0)
	diffs := []([]int){{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	maxX, maxY := len(lines[0])-1, len(lines)-1

	for len(possible) > 0 {
		coord, step := possible[0].coord, possible[0].step
		possible = possible[1:]

		if step > maxSteps {
			maxSteps = step
		}

		visited[coord] = step + 1
		x, y := coord.x, coord.y

		for _, diff := range diffs {
			dx, dy := diff[0], diff[1]
			nx, ny := x+dx, y+dy

			if nx < 0 || nx > maxX || ny < 0 || ny > maxY {
				continue
			}

			if checkPipeConnected(lines, x, y, nx, ny) && visited[Coord{nx, ny}] == 0 {
				possible = append(possible, CoordStep{Coord{nx, ny}, step + 1})
				visited[Coord{nx, ny}] = step + 1
			}
		}
	}

	return maxSteps
}

func parseL1(char rune) []rune {
	chars := []rune{}

	singles := []rune{'|', 'J', '7'}

	if slices.Contains(singles, char) {
		chars = append(chars, []rune{'*', ' '}...)
	} else {
		chars = append(chars, []rune{'*', '*'}...)
	}

	return chars
}

func parseL2(char rune) []rune {
	chars := []rune{}

	singles := []rune{'|', '7', 'F'}
	doubles := []rune{'S'}

	switch {
	case slices.Contains(singles, char):
		chars = append(chars, []rune{'*', ' '}...)
	case slices.Contains(doubles, char):
		chars = append(chars, []rune{'*', '*'}...)
	default:
		chars = append(chars, []rune{' ', ' '}...)
	}

	return chars
}

func upscaleGrid(lines []string) ([][]rune, []Coord) {
	doubleGrid := [][]rune{}
	nonBorder := []Coord{}

	for y, line := range lines {

		l1, l2 := []rune{}, []rune{}

		for x, char := range line {
			if visited[Coord{x, y}] != 0 {
				l1 = append(l1, parseL1(char)...)
				l2 = append(l2, parseL2(char)...)
			} else {
				l1 = append(l1, []rune{'.', ' '}...)
				l2 = append(l2, []rune{' ', ' '}...)

				nonBorder = append(nonBorder, Coord{x * 2, y * 2})
			}
		}

		doubleGrid = append(doubleGrid, l1)
		doubleGrid = append(doubleGrid, l2)
	}

	return doubleGrid, nonBorder
}

func checkEnclosed(doubleGrid [][]rune, coord Coord, free bool) bool {
	if visitedEnclosed[coord] != 0 {
		return free
	}

	visitedEnclosed[coord] = 1

	x, y := coord.x, coord.y
	xMax, yMax := len(doubleGrid[0])-1, len(doubleGrid)-1

	if x == 0 || x == xMax || y == 0 || y == yMax {
		free = true
	}

	diffs := []([]int){{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for _, diff := range diffs {
		dx, dy := diff[0], diff[1]
		nx, ny := x+dx, y+dy

		if nx < 0 || nx > xMax || ny < 0 || ny > yMax {
			continue
		}

		if doubleGrid[ny][nx] == ' ' || doubleGrid[ny][nx] == '.' {
			res := checkEnclosed(doubleGrid, Coord{nx, ny}, free)
			if res {
				free = res
			}
		}
	}

	if doubleGrid[y][x] == '.' {
		if !free {
			p2++
			doubleGrid[y][x] = 'I'
		} else {
			doubleGrid[y][x] = 'O'
		}
	}

	return free
}

func solve(lines []string) (int64, int64) {
	p1 = int64(0)
	p2 = int64(0)

	visited = make(map[Coord]int64)
	visitedEnclosed = make(map[Coord]int64)

	var start CoordStep

	for y, line := range lines {
		for x, char := range line {
			if char == 'S' {
				start = CoordStep{Coord{x, y}, 0}
				break
			}
		}
	}

	p1 = findFurthest(lines, []CoordStep{start})

	doubleGrid, nonBorder := upscaleGrid(lines)
	for _, coord := range nonBorder {
		checkEnclosed(doubleGrid, coord, false)
	}

	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 10\tPt1:\t%d\n", p1)
	fmt.Printf("Day 10\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
