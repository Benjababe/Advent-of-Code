package day14

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

type Coord struct {
	x int
	y int
}

type Obstacle int
type Direction int

const (
	Blank Obstacle = iota
	Rock
)

const (
	North Direction = iota
	West
	South
	East
)

func hashGrid(grid [][]string) string {
	hash, curChar, curCount := "", "", 0

	for _, line := range grid {
		for _, char := range line {
			if char != curChar {
				if curCount > 0 {
					hash += curChar + strconv.Itoa(curCount)
				}
				curCount = 1
				curChar = char
			} else {
				curCount++
			}
		}
		if curCount > 0 {
			hash += curChar + strconv.Itoa(curCount)
		}
		hash += "n"
	}

	return hash
}

func getGridLoad(grid [][]string) int64 {
	load := int64(0)
	for y, line := range grid {
		height := len(grid) - y
		for _, char := range line {
			if char == "O" {
				load += int64(height)
			}
		}
	}
	return load
}

func tiltVertical(grid [][]string, obstacles map[Coord]Obstacle, dir Direction) {
	maxY, stepY := -1, -1
	if dir == South {
		maxY, stepY = len(grid), 1
	}

	for y, line := range grid {
		for x, char := range line {
			if char != "O" {
				continue
			}

			finalY := -1
			for newY := y; newY != maxY; newY += stepY {
				newCoord := Coord{x, newY}
				if _, ok := obstacles[newCoord]; ok {
					if obstacles[newCoord] == Rock {
						break
					} else if obstacles[newCoord] == Blank {
						finalY = newY
					}
				}
			}

			if finalY != -1 {
				grid[y][x] = "."
				grid[finalY][x] = "O"
				delete(obstacles, Coord{x, finalY})
				obstacles[Coord{x, y}] = Blank
			}
		}
	}
}

func tiltHorizontal(grid [][]string, obstacles map[Coord]Obstacle, dir Direction) {
	maxX, stepX := -1, -1
	if dir == East {
		maxX, stepX = len(grid[0]), 1
	}

	for y, line := range grid {
		for x, char := range line {
			if char != "O" {
				continue
			}

			finalX := -1
			for newX := x; newX != maxX; newX += stepX {
				newCoord := Coord{newX, y}
				if _, ok := obstacles[newCoord]; ok {
					if obstacles[newCoord] == Rock {
						break
					} else if obstacles[newCoord] == Blank {
						finalX = newX
					}
				}
			}

			if finalX != -1 {
				grid[y][x] = "."
				grid[y][finalX] = "O"
				delete(obstacles, Coord{finalX, y})
				obstacles[Coord{x, y}] = Blank
			}
		}
	}
}

func cycleGrid(grid [][]string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	memoi := map[string]int{}
	obstacles := map[Coord]Obstacle{}
	cycles := 1000000000

	for y, line := range grid {
		for x, char := range line {
			switch char {
			case ".":
				obstacles[Coord{x, y}] = Obstacle(Blank)
			case "#":
				obstacles[Coord{x, y}] = Obstacle(Rock)
			}
		}
	}

	for i := 0; i < cycles; i++ {
		tiltVertical(grid, obstacles, Direction(North))
		if i == 0 {
			p1 = getGridLoad(grid)
		}

		tiltHorizontal(grid, obstacles, Direction(West))
		tiltVertical(grid, obstacles, Direction(South))
		tiltHorizontal(grid, obstacles, Direction(East))

		gridHash := hashGrid(grid)

		if _, ok := memoi[gridHash]; ok {
			prevCount := memoi[gridHash]
			cyclesNeeded := i - prevCount
			itersStillNeeded := ((cycles - i) % cyclesNeeded) - 1

			for j := 0; j < itersStillNeeded; j++ {
				tiltVertical(grid, obstacles, Direction(North))
				tiltHorizontal(grid, obstacles, Direction(West))
				tiltVertical(grid, obstacles, Direction(South))
				tiltHorizontal(grid, obstacles, Direction(East))
			}

			p2 = getGridLoad(grid)
			return p1, p2
		}

		memoi[gridHash] = i
	}

	return p1, p2
}

func solve(lines []string) (int64, int64) {
	grid := [][]string{}

	for _, line := range lines {
		line = strings.TrimSpace(line)
		grid = append(grid, strings.Split(line, ""))
	}

	p1, p2 := cycleGrid(grid)
	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 14\tPt1:\t%d\n", p1)
	fmt.Printf("Day 14\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
