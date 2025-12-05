package main

import (
	"fmt"
	"slices"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
	"golang.org/x/exp/maps"
)

type Instruction struct {
	from  string
	to    string
	pulse int
}

type Module struct {
	modType string
	state   int
	memory  map[string]int
	mods    []string
}

var btnPresses int64
var modules map[string]Module
var mainParentLoops map[string]int64
var donePt2 bool

func gcd(a, b int64) int64 {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func lcm(nums []int64) int64 {
	if len(nums) == 0 {
		panic("No numbers to lcm")
	} else if len(nums) == 1 {
		return nums[0]
	}

	res := nums[0] * nums[1] / gcd(nums[0], nums[1])

	for _, num := range nums[2:] {
		res = lcm([]int64{res, num})
	}

	return res
}

func sendPulse(instruction Instruction) []Instruction {
	more := []Instruction{}
	to, from := instruction.to, instruction.from

	if _, ok := modules[instruction.to]; !ok {
		return more
	}

	module := modules[instruction.to]
	modType, innerMods := module.modType, module.mods

	if modType == "ff" && instruction.pulse == 0 {
		newState := 0
		if module.state == 0 {
			newState = 1
		}
		module.state = newState
		modules[to] = module

		for _, innerMod := range innerMods {
			more = append(more, Instruction{to, innerMod, newState})
		}
	}

	if modType == "cjt" {
		module.memory[from] = instruction.pulse

		v := maps.Values(module.memory)
		ts := helper.SlicesAll[int](v, func(i int) bool { return i == 1 })
		toSend := 1
		if ts {
			toSend = 0
		}

		mainParents := []string{"mf", "fz", "ss", "fh"}
		if slices.Contains(mainParents, to) && toSend == 1 {
			if _, ok := mainParentLoops[to]; !ok {
				mainParentLoops[to] = btnPresses
			}
			if len(mainParentLoops) == len(mainParents) {
				donePt2 = true
			}
		}

		for _, innerMod := range innerMods {
			more = append(more, Instruction{to, innerMod, toSend})
		}
	}

	return more
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)

	btnPresses = int64(0)
	modules = map[string]Module{}
	mainParentLoops = map[string]int64{}
	donePt2 = false

	broadcast := []Instruction{}

	for _, line := range lines {
		if line[0] == 'b' {
			childrenStr := strings.TrimSpace(strings.Split(line, " -> ")[1])
			children := strings.Split(childrenStr, ", ")
			for _, child := range children {
				broadcast = append(broadcast, Instruction{"broadcaster", child, 0})
			}
		} else if line[0] == '%' {
			spl := strings.Split(line, " -> ")
			ff, mods := spl[0][1:], strings.Split(strings.TrimSpace(spl[1]), ", ")
			modules[ff] = Module{"ff", 0, map[string]int{}, mods}
		} else if line[0] == '&' {
			spl := strings.Split(line, " -> ")
			cjt, mods := spl[0][1:], strings.Split(strings.TrimSpace(spl[1]), ", ")
			modules[cjt] = Module{"cjt", 0, map[string]int{}, mods}
		}
	}

	for k, module := range modules {
		for _, inner := range module.mods {
			im := modules[inner]
			if im.modType == "cjt" {
				innerMod := modules[inner]
				innerMod.memory[k] = 0
				modules[inner] = innerMod
			}
		}
	}

	stateCounts := [2]int64{0, 0}

	for btnPresses = 1; btnPresses <= 1000 || !donePt2; btnPresses++ {
		if btnPresses < 1000 {
			stateCounts[0]++
		}
		queue := broadcast
		for len(queue) > 0 {
			instruction := queue[0]
			queue = queue[1:]

			if btnPresses < 1000 {
				stateCounts[instruction.pulse]++
			}

			more := sendPulse(instruction)
			queue = append(queue, more...)
		}
	}

	p1 = stateCounts[0] * stateCounts[1]
	p2 = lcm(maps.Values(mainParentLoops))

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
