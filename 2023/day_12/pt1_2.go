package main

import (
	"fmt"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

type MemoiKey struct {
	line      string
	groupsStr string
}

var memoi map[MemoiKey]int64

func getFirstGroupLen(line string, groupLength int64) int64 {
	count := int64(0)

	if groupLength > int64(len(line)) {
		return -1
	}

	for i := int64(0); i < groupLength; i++ {
		char := line[i]
		if char == '#' || char == '?' {
			count++
		} else {
			break
		}
	}

	return count
}

func iterGroups(line string, groups []int64) int64 {
	groupsStr := helper.SliceToString[int64](groups, "_")
	key := MemoiKey{line, groupsStr}
	value, exists := memoi[key]
	if exists {
		return value
	}

	if len(line) == 0 {
		if len(groups) == 0 {
			return 1
		} else {
			return 0
		}
	}

	if len(groups) == 0 {
		if strings.Contains(line, "#") {
			return 0
		} else {
			return 1
		}
	}

	total := int64(0)

	if line[0] == '.' {
		total += iterGroups(line[1:], groups)
	} else if line[0] == '?' {
		l1 := helper.StringReplaceIndex(line, 0, '#')
		l2 := helper.StringReplaceIndex(line, 0, '.')
		total += iterGroups(l1, groups)
		total += iterGroups(l2, groups)
	} else if line[0] == '#' {
		groupLength := getFirstGroupLen(line, groups[0])

		if groupLength == groups[0] {
			if groupLength < int64(len(line)) {
				if line[groupLength] == '#' {
					return 0
				} else {
					total += iterGroups(line[groupLength+1:], groups[1:])
				}
			} else {
				total += iterGroups(line[groupLength:], groups[1:])
			}
		} else {
			return 0
		}
	}

	memoi[key] = total
	return total
}

func solve(lines []string) (int64, int64) {
	p1, p2 := int64(0), int64(0)
	memoi = make(map[MemoiKey]int64)

	for _, line := range lines {
		lineSpl := strings.Split(strings.TrimSpace(line), " ")
		line, groupStr := lineSpl[0], lineSpl[1]
		groups := strings.Split(groupStr, ",")
		groupsI64, _ := helper.SliceStrToInt64(groups)

		p2LineSlice := []string{line, line, line, line, line}
		p2Line := strings.Join(p2LineSlice, "?")
		p2GroupsI64 := helper.SliceRepeat[int64](groupsI64, 5)

		p1 += iterGroups(line, groupsI64)
		p2 += iterGroups(p2Line, p2GroupsI64)
	}

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
