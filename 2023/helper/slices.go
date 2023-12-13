package helper

import (
	"fmt"
	"strconv"
)

// Use a predicate function and returns if all element in the slice matches it
func SlicesAll[T any](slice []T, pred func(T) bool) bool {
	for _, elem := range slice {
		if !pred(elem) {
			return false
		}
	}
	return true
}

// Use a predicate function and returns if any element in the slice matches it
func SlicesAny[T any](slice []T, pred func(T) bool) bool {
	for _, elem := range slice {
		if pred(elem) {
			return true
		}
	}
	return false
}

func SliceStrToInt64(slice []string) ([]int64, error) {
	int64Slice := make([]int64, len(slice))
	for i, elem := range slice {
		num, err := strconv.ParseInt(elem, 10, 64)
		if err != nil {
			return nil, err
		}

		int64Slice[i] = num
	}
	return int64Slice, nil
}

func SliceInt64ToStr(slice []int64) []string {
	strSlice := make([]string, len(slice))
	for i, elem := range slice {
		str := strconv.FormatInt(elem, 10)
		strSlice[i] = str
	}
	return strSlice
}

func SliceToString[T int | int64](slice []T, sep string) string {
	str := ""
	for _, v := range slice {
		str += fmt.Sprint(v) + sep
	}
	return str
}

func SliceRepeat[T int | int64 | string](slice []T, n int) []T {
	repeated := make([]T, 0)
	for i := 0; i < n; i++ {
		repeated = append(repeated, slice...)
	}
	return repeated
}

func SliceTranspose[T int | int64 | string](slice [][]T) [][]T {
	xl := len(slice[0])
	yl := len(slice)
	result := make([][]T, xl)
	for i := range result {
		result[i] = make([]T, yl)
	}
	for i := 0; i < xl; i++ {
		for j := 0; j < yl; j++ {
			result[i][j] = slice[j][i]
		}
	}
	return result
}
