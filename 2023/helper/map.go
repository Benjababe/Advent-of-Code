package helper

func ReadMapDefault[K comparable, V interface{}](m map[K]V, key K, defaultValue V) V {
	if val, ok := m[key]; ok {
		return val
	}
	return defaultValue
}
