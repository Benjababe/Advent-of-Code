package main

import (
	"fmt"
	"slices"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

type Coord struct {
	x int
	y int
}

type Direction struct {
	dx int
	dy int
	d  rune
}

var grid [][]string
var memoi map[Coord]int64
var maxPath []Coord

func traverse(coord Coord, path []Coord, p2 bool) {
	x, y := coord.x, coord.y
	dirs := []Direction{{-1, 0, 'l'}, {1, 0, 'r'}, {0, -1, 'u'}, {0, 1, 'd'}}

	if slices.Contains(path, coord) {
		return
	}

	memoi[coord] = int64(len(path))
	tmpPath := slices.Clone(path)
	tmpPath = append(tmpPath, coord)

	if x == len(grid[0])-2 && y == len(grid)-1 && len(path) > len(maxPath) {
		maxPath = path
	}

	for _, dir := range dirs {
		dx, dy, d := dir.dx, dir.dy, dir.d
		nx, ny := x+dx, y+dy

		if nx < 0 || nx >= len(grid[0]) ||
			ny < 0 || ny >= len(grid) || grid[ny][nx] == "#" {
			continue
		}

		if !p2 {
			if grid[y][x] == "<" && d != 'l' ||
				grid[y][x] == ">" && d != 'r' ||
				grid[y][x] == "^" && d != 'u' ||
				grid[y][x] == "v" && d != 'd' {
				continue
			}
		}

		traverse(Coord{nx, ny}, tmpPath, p2)
	}
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	grid = [][]string{}

	for _, line := range lines {
		gridLine := strings.Split(strings.TrimSpace(line), "")
		grid = append(grid, gridLine)
	}

	memoi = map[Coord]int64{}
	maxPath = []Coord{}
	traverse(Coord{1, 0}, []Coord{}, false)
	p1 = int64(len(maxPath))

	memoi = map[Coord]int64{}
	maxPath = []Coord{}
	traverse(Coord{1, 0}, []Coord{}, true)
	p2 = int64(len(maxPath))

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
