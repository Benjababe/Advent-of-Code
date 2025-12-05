package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

type Hand struct {
	bid   int64
	score int64
	hand  string
}

var cardOrder = "23456789TJQKA"
var comboScores = map[string]int64{
	"highCard":     1,
	"onePair":      2,
	"twoPair":      3,
	"threeOfAKind": 4,
	"fullHouse":    5,
	"fourOfAKind":  6,
	"fiveOfAKind":  7,
}

func getHandScore(hand string) int64 {
	hScore := int64(0)
	comboCounts := [6]int{0, 0, 0, 0, 0, 0}

	curChar, curCount := '0', 0
	hand += " "

	for _, char := range hand {
		if char == curChar {
			curCount += 1
		} else {
			comboCounts[curCount] += 1
			curChar = char
			curCount = 1
		}
	}

	if comboCounts[2] == 1 && comboCounts[3] == 0 {
		hScore = comboScores["onePair"]
	} else if comboCounts[2] == 2 {
		hScore = comboScores["twoPair"]
	} else if comboCounts[2] == 0 && comboCounts[3] == 1 {
		hScore = comboScores["threeOfAKind"]
	} else if comboCounts[2] == 1 && comboCounts[3] == 1 {
		hScore = comboScores["fullHouse"]
	} else if comboCounts[4] == 1 {
		hScore = comboScores["fourOfAKind"]
	} else if comboCounts[5] == 1 {
		hScore = comboScores["fiveOfAKind"]
	} else {
		hScore = comboScores["highCard"]
	}

	return hScore
}

func cmpHandString(h1, h2 string) bool {
	for i := range h1 {
		c1, c2 := string(h1[i]), string(h2[i])
		i1, i2 := strings.Index(cardOrder, c1), strings.Index(cardOrder, c2)

		if i1 == i2 {
			continue
		} else {
			return i1 < i2
		}
	}

	return false
}

func sortHands(hands []Hand) {
	sort.Slice(hands, func(i, j int) bool {
		if hands[i].score == hands[j].score {
			return cmpHandString(hands[i].hand, hands[j].hand)
		}

		return hands[i].score < hands[j].score
	})
}

func solve(lines []string) int64 {
	score := int64(0)
	hands := []Hand{}

	for _, line := range lines {
		lineSpl := strings.Split(line, " ")
		handStr, bidStr := lineSpl[0], lineSpl[1]

		bid, _ := strconv.ParseInt(bidStr, 10, 64)
		handScore := getHandScore(helper.SortString(handStr))

		hands = append(hands, Hand{bid, handScore, handStr})
	}

	sortHands(hands)
	for i, hand := range hands {
		score += int64(i+1) * hand.bid
	}

	return score
}

func main() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solve(lines)
	fmt.Printf("Output: %d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)

	helper.CopyClipboard(strconv.FormatInt(output, 10))
}
