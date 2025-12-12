package day18

import (
	"fmt"
	"math"
	"regexp"
	"strconv"

	"github.com/benjababe/advent-of-code/helper"
)

type Instruction struct {
	dir   string
	steps int64
}

type Vertex struct {
	x int64
	y int64
}

func polygonArea(vertices []Vertex) int64 {
	area := float64(0)
	n := len(vertices)

	for i := 0; i < n; i++ {
		j := (i + 1) % n
		area += float64(vertices[i].x * vertices[j].y)
		area -= float64(vertices[j].x * vertices[i].y)
	}

	area = math.Abs(area) / 2
	return int64(area)
}

func parseLine(line string, hex bool) Instruction {
	instruction := Instruction{}
	r := regexp.MustCompile(`(\w)\s(\d+)\s\(#([\d\w]{5})(\d)\)`)
	matches := r.FindStringSubmatch(line)

	dirMap := map[string]string{"0": "R", "1": "D", "2": "L", "3": "U"}

	if hex {
		instruction.steps, _ = strconv.ParseInt(matches[3], 16, 64)
		instruction.dir = dirMap[matches[4]]
	} else {
		instruction.steps, _ = strconv.ParseInt(matches[2], 10, 64)
		instruction.dir = matches[1]
	}

	return instruction
}

func dig(lines []string, hex bool) int64 {
	x, y := int64(0), int64(0)
	vertices := []Vertex{}
	borderLen := int64(0)

	for _, line := range lines {
		instruction := parseLine(line, hex)

		switch instruction.dir {
		case "L":
			x -= instruction.steps
		case "R":
			x += instruction.steps
		case "U":
			y -= instruction.steps
		case "D":
			y += instruction.steps
		}

		vertices = append(vertices, Vertex{x, y})
		borderLen += instruction.steps
	}

	area := polygonArea(vertices)
	area += borderLen/2 + 1

	return area
}

func solve(lines []string) (int64, int64) {
	p1, p2 := dig(lines, false), dig(lines, true)
	return p1, p2
}

func Solve() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1, p2 := solve(lines)
	fmt.Printf("Day 18\tPt1:\t%d\n", p1)
	fmt.Printf("Day 18\tPt2:\t%d\n", p2)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
