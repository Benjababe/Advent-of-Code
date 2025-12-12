package day21

import (
	"fmt"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

type Coord struct {
	x int
	y int
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	grid := [][]rune{}
	queue := []Coord{}
	directions := []Coord{{0, 1}, {-1, 0}, {0, -1}, {1, 0}}

	for y, line := range lines {
		gridLine := []rune{}
		for x, char := range strings.TrimSpace(line) {
			gridLine = append(gridLine, char)

			if char == 'S' {
				queue = append(queue, Coord{x, y})
			}
		}
		grid = append(grid, gridLine)
	}

	stepPlot := []int{}
	maxPt1 := 64
	maxPt2 := 26501365
	for i := 1; i < maxPt2; i++ {
		nextQueue := []Coord{}
		visited := map[Coord]int{}

		for len(queue) > 0 {
			coord := queue[0]
			queue = queue[1:]

			for _, dir := range directions {
				nCoord := Coord{coord.x + dir.x, coord.y + dir.y}
				nCoordRef := Coord{nCoord.x % len(grid[0]), nCoord.y % len(grid)}

				for nCoordRef.x < 0 {
					nCoordRef.x += len(grid[0])
				}

				for nCoordRef.y < 0 {
					nCoordRef.y += len(grid)
				}

				if grid[nCoordRef.y][nCoordRef.x] != '#' {
					if _, ok := visited[nCoord]; !ok {
						visited[nCoord] = 1
						nextQueue = append(nextQueue, nCoord)
					}
				}
			}
		}

		if (i % len(grid)) == (maxPt2 % len(grid)) {
			fmt.Printf("Loop: %d,\tPositions: %d\n", len(stepPlot), len(visited))
			stepPlot = append(stepPlot, len(visited))

			if len(stepPlot) == 4 {
				fmt.Println("Enter the above into a polynomial fitter to get a quadratic expression")
				break
			}
		}

		if i == maxPt1 {
			p1 = int64(len(visited))
		}

		queue = nextQueue
	}

	// Plug in polynomial values here, where the polynomial is:
	// ax^2 + bx + c
	a, b, c := int64(14812), int64(14925), int64(3759)

	x := int64(maxPt2 / len(grid))
	p2 = a*x*x + b*x + c

	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 21\tPt1:\t%d\n", p1)
	fmt.Printf("Day 21\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
