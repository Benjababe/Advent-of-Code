package helper

import (
	"fmt"
	"time"
)

func GetCurrentTime() time.Time {
	return time.Now()
}

func GetTimeTaken(start time.Time, stop time.Time) {
	units := []string{"", "milli", "micro", "nano"}
	uIndex := 0

	timeTaken := stop.Sub(start).Seconds()

	for timeTaken > 0 && timeTaken < 1.0 {
		timeTaken *= 1000
		uIndex++
	}

	fmt.Printf("Program running time: %f %sseconds\n", timeTaken, units[uIndex])
}
