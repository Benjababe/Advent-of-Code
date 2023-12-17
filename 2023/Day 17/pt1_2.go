package main

import (
	"fmt"

	"github.com/benjababe/advent-of-code/helper"
	"github.com/gammazero/deque"
)

var grid [][]int64

type Vector struct {
	x int
	y int
}

type State struct {
	x   int
	y   int
	dir string
}

type DequeItem struct {
	x     int
	y     int
	dir   rune
	score int64
}

func traverse() (int64, int64) {
	scores := [2]int64{1e10, 1e10}

	nextDirs := map[rune]string{'l': "ud", 'r': "ud", 'u': "lr", 'd': "lr"}
	opposite := map[rune]string{'l': "lr", 'r': "lr", 'u': "ud", 'd': "ud"}
	dirs := map[rune]Vector{'l': {-1, 0}, 'r': {1, 0}, 'u': {0, -1}, 'd': {0, 1}}

	maxX, maxY := len(grid[0])-1, len(grid)-1

	for i, stepRange := range [][]int{{1, 3}, {4, 10}} {
		memoi := map[State]int64{}
		dq := deque.Deque[DequeItem]{}
		dq.PushFront(DequeItem{0, 0, 'l', 0})
		dq.PushFront(DequeItem{0, 0, 'd', 0})

		for dq.Len() > 0 {
			dqItem := dq.PopBack()
			x, y, dir, score := dqItem.x, dqItem.y, dqItem.dir, dqItem.score

			oppo := opposite[dir]
			prev, ok := memoi[State{x, y, oppo}]
			if ok && prev <= score {
				continue
			}

			if x == maxX && y == maxY && score < scores[i] {
				scores[i] = score
			}

			memoi[State{x, y, oppo}] = score

			for _, nextDir := range nextDirs[dir] {
				nextScore := int64(0)
				dirChange := dirs[nextDir]
				dx, dy := dirChange.x, dirChange.y

				for l := 1; l <= stepRange[1]; l++ {
					xx, yy := x+l*dx, y+l*dy

					if 0 <= xx && xx <= maxX && 0 <= yy && yy <= maxY {
						nextScore += grid[yy][xx]
						if l >= stepRange[0] {
							dq.PushFront(DequeItem{xx, yy, nextDir, score + nextScore})
						}
					}
				}
			}
		}
	}

	return scores[0], scores[1]
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	grid = [][]int64{}

	for _, line := range lines {
		row := []int64{}
		for _, char := range line {
			row = append(row, int64(char-'0'))
		}
		grid = append(grid, row)
	}

	p1, p2 = traverse()

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
