package main

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/benjababe/advent-of-code/helper"
)

type FarmMap = map[string](map[string][]FarmTransform)
type CatMap = map[string]string

type FarmTransform struct {
	srcStart int64
	dstStart int64
	rng      int64
}

type SeedPair struct {
	start int64
	rng   int64
}

func populateMaps(farmMap FarmMap, categoryMap CatMap, lines []string) {
	from, to := "", ""
	mapRegex := regexp.MustCompile(`(\w+)-to-(\w+) map:`)
	rngRegex := regexp.MustCompile(`(\d+) (\d+) (\d+)`)

	for _, line := range lines[1:] {
		if line == "" || line == "\n" {
			continue
		}

		mapMatch := mapRegex.FindStringSubmatch(line)
		if mapMatch != nil {
			from, to = mapMatch[1], mapMatch[2]
			farmMap[to] = make(map[string][]FarmTransform)
			farmMap[to][from] = make([]FarmTransform, 0)
			categoryMap[to] = from
			continue
		}

		rngMatch := rngRegex.FindStringSubmatch(line)
		if rngMatch != nil {
			srcStart, _ := strconv.ParseInt(rngMatch[1], 10, 64)
			dstStart, _ := strconv.ParseInt(rngMatch[2], 10, 64)
			rng, _ := strconv.ParseInt(rngMatch[3], 10, 64)

			tfs := farmMap[to][from]
			tfs = append(tfs, FarmTransform{srcStart, dstStart, rng})
			farmMap[to][from] = tfs
		}
	}
}

func getLowestLocation(farmMap FarmMap, categoryMap CatMap, seedPairs []SeedPair) int64 {
	for loc := int64(0); loc < 1e11; loc++ {
		category := "location"
		catVal := loc

		for category != "seed" {
			newCategory := categoryMap[category]

			for _, tsf := range farmMap[category][newCategory] {
				if tsf.srcStart <= catVal && catVal <= (tsf.srcStart+tsf.rng) {
					catVal = catVal - tsf.srcStart + tsf.dstStart
					break
				}
			}

			category = newCategory
		}

		for _, seedPair := range seedPairs {
			if seedPair.start <= catVal && catVal <= seedPair.start+seedPair.rng {
				return loc
			}
		}
	}

	return -1
}

func solve(lines []string) int64 {
	score := int64(0)

	farmMap := make(FarmMap)
	categoryMap := make(CatMap)

	populateMaps(farmMap, categoryMap, lines)

	seeds := make([]SeedPair, 0)
	seedRegex := regexp.MustCompile(`(\d+)\s(\d+)`)
	seedMatches := seedRegex.FindAllStringSubmatch(lines[0], -1)
	for _, seedMatch := range seedMatches {
		seedStart, _ := strconv.ParseInt(seedMatch[1], 10, 64)
		seedRange, _ := strconv.ParseInt(seedMatch[2], 10, 64)
		seeds = append(seeds, SeedPair{seedStart, seedRange})
	}
	score = getLowestLocation(farmMap, categoryMap, seeds)

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
