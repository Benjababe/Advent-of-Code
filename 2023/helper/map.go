package helper

func ReadMapDefault[K comparable, V interface{}](m map[K]V, key K, defaultValue V) V {
	if val, ok := m[key]; ok {
		return val
	}
	return defaultValue
}

func SetUnion[K comparable](m1, m2 map[K]bool) map[K]bool {
	unionMap := make(map[K]bool)
	for k := range m1 {
		unionMap[k] = true
	}
	for k := range m2 {
		unionMap[k] = true
	}
	return unionMap
}

func SetIntersect[K comparable](m1, m2 map[K]bool) map[K]bool {
	intersectSet := make(map[K]bool)
	for k := range m1 {
		if _, ok := m2[k]; ok {
			intersectSet[k] = true
		}
	}
	return intersectSet
}
