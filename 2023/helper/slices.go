package helper

import "strconv"

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
