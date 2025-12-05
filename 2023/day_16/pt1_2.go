package main

import (
	"fmt"

	"github.com/benjababe/advent-of-code/helper"
)

type Coord struct {
	x int
	y int
}

type Velocity struct {
	dx int
	dy int
}

type Ray struct {
	coord Coord
	velo  Velocity
}

var grid [][]rune

func handleCell(cell rune, ray Ray) []Ray {
	x, y := ray.coord.x, ray.coord.y
	dx, dy := ray.velo.dx, ray.velo.dy

	if cell == '/' {
		dx, dy = -dy, -dx
		newCoord := Coord{x + dx, y + dy}
		return []Ray{{newCoord, Velocity{dx, dy}}}
	} else if cell == '\\' {
		dx, dy = dy, dx
		newCoord := Coord{x + dx, y + dy}
		return []Ray{{newCoord, Velocity{dx, dy}}}
	} else if cell == '-' && dx == 0 {
		return []Ray{
			{Coord{x - 1, y}, Velocity{-1, 0}},
			{Coord{x + 1, y}, Velocity{1, 0}},
		}
	} else if cell == '|' && dy == 0 {
		return []Ray{
			{Coord{x, y - 1}, Velocity{0, -1}},
			{Coord{x, y + 1}, Velocity{0, 1}},
		}
	} else {
		newCoord := Coord{x + dx, y + dy}
		return []Ray{{newCoord, ray.velo}}
	}
}

func rayTrace(ray Ray) int64 {
	rays := []Ray{ray}
	energyMap := map[Coord]bool{}
	memoi := map[Ray]bool{}

	for len(rays) > 0 {
		newRays := []Ray{}

		for _, ray := range rays {
			x, y := ray.coord.x, ray.coord.y

			if memoi[ray] ||
				x < 0 ||
				x >= len(grid[0]) ||
				y < 0 ||
				y >= len(grid) {
				continue
			}

			memoi[ray] = true
			energyMap[ray.coord] = true
			cell := grid[y][x]

			tmpRays := handleCell(cell, ray)
			newRays = append(newRays, tmpRays...)
		}

		rays = newRays
	}

	return int64(len(energyMap))
}

func rayTraceBorders() int64 {
	maxScore := int64(0)
	maxX := len(grid[0]) - 1
	maxY := len(grid) - 1

	for x := 0; x <= maxX; x++ {
		rays := Ray{Coord{x, 0}, Velocity{0, 1}}
		tmp := rayTrace(rays)
		if tmp > maxScore {
			maxScore = tmp
		}

		rays = Ray{Coord{x, maxX}, Velocity{0, -1}}
		tmp = rayTrace(rays)
		if tmp > maxScore {
			maxScore = tmp
		}
	}

	for y := 0; y <= maxY; y++ {
		rays := Ray{Coord{0, y}, Velocity{1, 0}}
		tmp := rayTrace(rays)
		if tmp > maxScore {
			maxScore = tmp
		}

		rays = Ray{Coord{maxY, y}, Velocity{-1, 0}}
		tmp = rayTrace(rays)
		if tmp > maxScore {
			maxScore = tmp
		}
	}

	return maxScore
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	grid = [][]rune{}

	for _, line := range lines {
		gridLine := []rune{}
		for _, char := range line {
			gridLine = append(gridLine, char)
		}
		grid = append(grid, gridLine)
	}

	p1 = rayTrace(Ray{Coord{0, 0}, Velocity{1, 0}})
	p2 = rayTraceBorders()

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
