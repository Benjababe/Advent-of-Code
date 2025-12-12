package day06

import (
	"fmt"
	"math"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

func getButtonCombinations(time string, dist string) int64 {
	timeInt, _ := strconv.ParseFloat(time, 64)
	distInt, _ := strconv.ParseFloat(dist, 64)

	disc := timeInt*timeInt - 4*-distInt*-1
	x1 := math.Floor((-timeInt + math.Sqrt(disc)) / -2)
	x2 := math.Floor((-timeInt - math.Sqrt(disc)) / -2)

	return int64(x2 - x1)
}

func solve(lines []string) {
	scores := []int64{1, 0}

	time, dist := lines[0], lines[1]
	times := strings.Fields(strings.Split(time, ":")[1])
	dists := strings.Fields(strings.Split(dist, ":")[1])
	cTime := strings.ReplaceAll(strings.Split(time, ":")[1], " ", "")
	cDist := strings.ReplaceAll(strings.Split(dist, ":")[1], " ", "")

	for i, time := range times {
		scores[0] *= getButtonCombinations(time, dists[i])
	}
	scores[1] = getButtonCombinations(cTime, cDist)

	fmt.Printf("Day 6\tPt1:\t%d\n", scores[0])
	fmt.Printf("Day 6\tPt2:\t%d\n", scores[1])
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	solve(lines)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
