package day07

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/benjababe/advent-of-code/helper"
)

var cardOrder2 = "J23456789TQKA"
var jCountMap = map[string][]int64{
	"highCard":     {1, 2, 4, 6, 7, 7},
	"onePair":      {2, 4, 6, 7, 7, 7},
	"twoPair":      {3, 5, 7, 7, 7, 7},
	"threeOfAKind": {4, 6, 7, 7, 7, 7},
	"fullHouse":    {5, 5, 5, 5, 5, 5},
	"fourOfAKind":  {6, 7, 7, 7, 7, 7},
	"fiveOfAKind":  {7, 7, 7, 7, 7, 7},
}

func getHandScore2(hand string) int64 {
	hScore := int64(0)
	comboCounts := [6]int{0, 0, 0, 0, 0, 0}

	sortedHand := helper.SortString(hand)

	comboType := ""
	curChar, curCount, jCount := '0', 0, int64(0)
	sortedHand += " "

	for _, char := range sortedHand {
		switch char {
		case 'J':
			jCount++
		case curChar:
			curCount++
		default:
			comboCounts[curCount]++
			curChar = char
			curCount = 1
		}
	}

	switch {
	case comboCounts[2] == 1 && comboCounts[3] == 0:
		comboType = "onePair"
	case comboCounts[2] == 2:
		comboType = "twoPair"
	case comboCounts[2] == 0 && comboCounts[3] == 1:
		comboType = "threeOfAKind"
	case comboCounts[2] == 1 && comboCounts[3] == 1:
		comboType = "fullHouse"
	case comboCounts[4] == 1:
		comboType = "fourOfAKind"
	case comboCounts[5] == 1:
		comboType = "fiveOfAKind"
	default:
		comboType = "highCard"
	}

	hScore = jCountMap[comboType][jCount]
	return hScore
}

func solvePt2(lines []string) int64 {
	score := int64(0)
	hands := []Hand{}

	for _, line := range lines {
		lineSpl := strings.Split(line, " ")
		handStr, bidStr := lineSpl[0], lineSpl[1]

		bid, _ := strconv.ParseInt(bidStr, 10, 64)
		handScore := getHandScore2(handStr)

		hands = append(hands, Hand{bid, handScore, handStr})
	}

	sortHands(hands, cardOrder2)
	for i, hand := range hands {
		score += int64(i+1) * hand.bid
	}

	return score
}

func Pt2() {
	lines := []string{}
	helper.GetLines(&lines, "input.txt")

	start := helper.GetCurrentTime()
	output := solvePt2(lines)
	fmt.Printf("Day 7\tPt2:\t%d\n", output)
	end := helper.GetCurrentTime()
	helper.GetTimeTaken(start, end)
}
