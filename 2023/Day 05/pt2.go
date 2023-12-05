package main

import (
	"fmt"
	"regexp"
	"strconv"
	"sync"

	"github.com/benjababe/advent-of-code/helper"
)

type FarmMap = map[string](map[string][]FarmTransform)
type CatMap = map[string]string

type FarmTransform struct {
	dstStart int64
	srcStart int64
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
			farmMap[from] = make(map[string][]FarmTransform)
			farmMap[from][to] = make([]FarmTransform, 0)
			categoryMap[from] = to
			continue
		}

		rngMatch := rngRegex.FindStringSubmatch(line)
		if rngMatch != nil {
			dstStart, _ := strconv.ParseInt(rngMatch[1], 10, 64)
			srcStart, _ := strconv.ParseInt(rngMatch[2], 10, 64)
			rng, _ := strconv.ParseInt(rngMatch[3], 10, 64)

			tfs := farmMap[from][to]
			tfs = append(tfs, FarmTransform{dstStart, srcStart, rng})
			farmMap[from][to] = tfs
		}
	}
}

func iterateSeedPair(farmMap FarmMap, categoryMap CatMap, seedPair SeedPair, lowest *int64, wg *sync.WaitGroup) {
	for inc := int64(0); inc < seedPair.rng; inc++ {
		category := "seed"
		seedVal := seedPair.start + inc
		catVal := seedVal

		for category != "location" {
			newCategory := categoryMap[category]

			for _, tsf := range farmMap[category][newCategory] {
				if tsf.srcStart <= catVal && catVal <= (tsf.srcStart+tsf.rng) {
					catVal = catVal - tsf.srcStart + tsf.dstStart
					break
				}
			}

			category = newCategory
		}

		if catVal < *lowest {
			*lowest = catVal
			fmt.Printf("New lowest location is %d with seed %d\n", catVal, seedVal)
		}
	}
	wg.Done()
}

func getLowestLocation(farmMap FarmMap, categoryMap CatMap, seedPairs []SeedPair) int64 {
	lowest := int64(1e11)
	var wg sync.WaitGroup

	for _, seedPair := range seedPairs {
		wg.Add(1)
		go iterateSeedPair(farmMap, categoryMap, seedPair, &lowest, &wg)
	}
	wg.Wait()

	return lowest
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
