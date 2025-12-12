package main

import (
	"slices"

	day01 "github.com/benjababe/advent-of-code/day_01"
	day02 "github.com/benjababe/advent-of-code/day_02"
	day03 "github.com/benjababe/advent-of-code/day_03"
	day04 "github.com/benjababe/advent-of-code/day_04"
	day05 "github.com/benjababe/advent-of-code/day_05"
	day06 "github.com/benjababe/advent-of-code/day_06"
	day07 "github.com/benjababe/advent-of-code/day_07"
	day08 "github.com/benjababe/advent-of-code/day_08"
	day09 "github.com/benjababe/advent-of-code/day_09"
	day10 "github.com/benjababe/advent-of-code/day_10"
	day11 "github.com/benjababe/advent-of-code/day_11"
	day12 "github.com/benjababe/advent-of-code/day_12"
	day13 "github.com/benjababe/advent-of-code/day_13"
	day14 "github.com/benjababe/advent-of-code/day_14"
	day15 "github.com/benjababe/advent-of-code/day_15"
	day16 "github.com/benjababe/advent-of-code/day_16"
	day17 "github.com/benjababe/advent-of-code/day_17"
	day18 "github.com/benjababe/advent-of-code/day_18"
	day20 "github.com/benjababe/advent-of-code/day_20"
	day21 "github.com/benjababe/advent-of-code/day_21"
	day23 "github.com/benjababe/advent-of-code/day_23"
	day24 "github.com/benjababe/advent-of-code/day_24"
)

func main() {
	days := []int{}
	for i := range 26 {
		if slices.Contains([]int{8, 19, 22, 25}, i) {
			continue
		}
		days = append(days, i)
	}

	for _, day := range days {
		switch day {
		case 1:
			day01.Pt1()
			day01.Pt2()
		case 2:
			day02.Pt1()
			day02.Pt2()
		case 3:
			day03.Pt1()
			day03.Pt2()
		case 4:
			day04.Pt1()
			day04.Pt2()
		case 5:
			day05.Pt1()
			day05.Pt2()
		case 6:
			day06.Solve()
		case 7:
			day07.Pt1()
			day07.Pt2()
		case 8:
			day08.Pt1()
			day08.Pt2()
		case 9:
			day09.Solve()
		case 10:
			day10.Solve()
		case 11:
			day11.Solve()
		case 12:
			day12.Solve()
		case 13:
			day13.Solve()
		case 14:
			day14.Solve()
		case 15:
			day15.Solve()
		case 16:
			day16.Solve()
		case 17:
			day17.Solve()
		case 18:
			day18.Solve()
		case 20:
			day20.Solve()
		case 21:
			day21.Solve()
		case 23:
			day23.Solve()
		case 24:
			day24.Solve()
		}
	}
}
