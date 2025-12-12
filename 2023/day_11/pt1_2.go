package day11

import (
	"fmt"
	"math"

	"github.com/benjababe/advent-of-code/helper"
)

type Coord struct {
	x int
	y int
}

func getNewCoords(lines []string) ([]Coord, []Coord) {
	expandRows, expandCols := []bool{}, []bool{}
	p1Scale, p2Scale := 1, 999999
	p1Coords, p2Coords := []Coord{}, []Coord{}

	for y, line := range lines {
		expandRows = append(expandRows, true)

		for x, cell := range line {
			if len(expandCols) <= x {
				expandCols = append(expandCols, true)
			}

			if cell == '#' {
				expandRows[y] = false
				expandCols[x] = false
			}
		}
	}

	yOffset := 0
	for y, line := range lines {
		if expandRows[y] {
			yOffset++
		}

		xOffset := 0
		for x, cell := range line {
			if expandCols[x] {
				xOffset++
			}

			if cell == '#' {
				p1Coords = append(p1Coords, Coord{x + xOffset*p1Scale, y + yOffset*p1Scale})
				p2Coords = append(p2Coords, Coord{x + xOffset*p2Scale, y + yOffset*p2Scale})
			}
		}
	}

	return p1Coords, p2Coords
}

func findDistances(coords []Coord) int64 {
	distances := int64(0)

	for i, c1 := range coords {
		for _, c2 := range coords[i+1:] {
			dy := float64(c2.y - c1.y)
			dx := float64(c2.x - c1.x)
			distance := math.Abs(dy) + math.Abs(dx)
			distances += int64(distance)
		}
	}

	return distances
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	p1Coords, p2Coords := getNewCoords(lines)
	p1 = findDistances(p1Coords)
	p2 = findDistances(p2Coords)

	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 11\tPt1:\t%d\n", p1)
	fmt.Printf("Day 11\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
