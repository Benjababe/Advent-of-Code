package day13

import (
	"fmt"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func checkLeftRight(grid []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	for mirror := 1; mirror < len(grid[0]); mirror++ {
		sRange := min(mirror, len(grid[0])-mirror)
		l, r := mirror-1, mirror

		count := int64(0)

		for dx := 0; dx < sRange; dx++ {
			for _, line := range grid {
				nl, nr := l-dx, r+dx

				if line[nl] == line[nr] {
					count++
				}
			}
		}

		maxCount := int64(sRange * len(grid))
		switch count {
		case maxCount:
			p1 = int64(mirror)
		case maxCount - 1:
			p2 = int64(mirror)
		}
	}

	return p1, p2
}

func checkUpDown(grid []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	for mirror := 1; mirror < len(grid); mirror++ {
		sRange := min(mirror, len(grid)-mirror)
		up, dn := mirror-1, mirror

		count := 0

		for dy := 0; dy < sRange; dy++ {
			nUp, nDn := up-dy, dn+dy
			lineUp, lineDown := grid[nUp], grid[nDn]

			for i := 0; i < len(lineUp); i++ {
				c1, c2 := lineUp[i], lineDown[i]
				if c1 == c2 {
					count++
				}
			}
		}

		maxCount := sRange * len(grid[0])
		switch count {
		case maxCount:
			p1 = int64(mirror)
		case maxCount - 1:
			p2 = int64(mirror)
		}
	}

	return p1, p2
}

func checkGrid(grid []string) (int64, int64) {
	lr1, lr2 := checkLeftRight(grid)
	ud1, ud2 := checkUpDown(grid)

	return lr1 + ud1*100, lr2 + ud2*100
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	grid := []string{}

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" && len(grid) > 0 {
			res1, res2 := checkGrid(grid)
			p1 += res1
			p2 += res2
			grid = nil
		} else {
			grid = append(grid, strings.TrimSpace(line))
		}
	}

	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 13\tPt1:\t%d\n", p1)
	fmt.Printf("Day 13\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
