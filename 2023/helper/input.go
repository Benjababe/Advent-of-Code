package helper

import (
	"os"
	"path"
	"runtime"
	"strings"
)

func GetLines(lines *[]string, relFilePath string) {
	// Docs: https://golang.org/pkg/runtime/#Caller
	_, filename, _, ok := runtime.Caller(1)
	if !ok {
		panic("Could not find Caller of helper.GetLines")
	}

	absPath := path.Join(path.Dir(filename), relFilePath)

	content, err := os.ReadFile(absPath)
	if err != nil {
		panic(err)
	}

	strContent := strings.ReplaceAll(string(content), "\r\n", "\n")
	*lines = strings.Split(strContent, "\n")
}
