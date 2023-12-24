package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

type Vec3 struct {
	x float64
	y float64
	z float64
}

type Stone struct {
	start    Vec3
	velocity Vec3
}

type Boundary struct {
	l float64
	r float64
}

func checkIntersect2D(s1, s2 Stone, boundary Boundary) bool {
	p1, v1, p2, v2 := s1.start, s1.velocity, s2.start, s2.velocity
	m1, m2 := v1.y/v1.x, v2.y/v2.x

	// If parallel, they will never meet
	if m1 == m2 {
		return false
	}

	// Funky calculations off google
	x := (m1*p1.x - m2*p2.x + p2.y - p1.y) / (m1 - m2)
	y := (m1*m2*(p2.x-p1.x) + m2*p1.y - m1*p2.y) / (m2 - m1)

	t1 := (x - p1.x) / v1.x
	t2 := (x - p2.x) / v2.x

	// Won't meet if time is negative
	// Ignore if outside boundary
	if (t1 < 0 || t2 < 0) ||
		(x < boundary.l || x > boundary.r) ||
		(y < boundary.l || y > boundary.r) {
		return false
	}

	return true
}

func countCollisions2D(stones []Stone) int64 {
	collisions := int64(0)
	boundary := Boundary{200000000000000, 400000000000000}

	for i := 0; i < len(stones)-1; i++ {
		for j := i + 1; j < len(stones); j++ {
			s1, s2 := stones[i], stones[j]
			intersect := checkIntersect2D(s1, s2, boundary)
			if intersect {
				collisions++
			}
		}
	}

	return collisions
}

func solve(lines []string) int64 {
	p1 := int64(0)
	stones := []Stone{}

	for _, line := range lines {
		pattern := regexp.MustCompile(`(-*\d+),\s+(-*\d+),\s+(-*\d+)\s+@\s+(-*\d+),\s+(-*\d+),\s+(-*\d+)`)
		matches := pattern.FindStringSubmatch(strings.TrimSpace(line))

		x1, _ := strconv.ParseFloat(matches[1], 64)
		x2, _ := strconv.ParseFloat(matches[2], 64)
		x3, _ := strconv.ParseFloat(matches[3], 64)
		v1, _ := strconv.ParseFloat(matches[4], 64)
		v2, _ := strconv.ParseFloat(matches[5], 64)
		v3, _ := strconv.ParseFloat(matches[6], 64)

		stone := Stone{Vec3{x1, x2, x3}, Vec3{v1, v2, v3}}
		stones = append(stones, stone)
	}

	p1 = countCollisions2D(stones)
	return p1
}

func main() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	p1 := solve(lines)
	fmt.Printf("Silver: %d\n", p1)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
