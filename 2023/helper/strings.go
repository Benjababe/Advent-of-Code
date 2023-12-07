package helper

import "sort"

func SortString(s string) string {
	chars := []rune(s)
	sort.Slice(chars, func(i int, j int) bool {
		return chars[i] < chars[j]
	})
	return string(chars)
}
