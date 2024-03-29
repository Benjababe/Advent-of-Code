package helper

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path"
	"runtime"
	"strings"

	"golang.design/x/clipboard"
)

func GetLines(lines *[]string, relFilePath string) {
	// Docs: https://golang.org/pkg/runtime/#Caller
	_, filename, _, ok := runtime.Caller(1)
	if !ok {
		panic("Could not find Caller of helper.GetLines")
	}

	absPath := path.Join(path.Dir(filename), relFilePath)

	_, err := os.Stat(absPath)
	if os.IsNotExist(err) {
		panic("File does not exist!")
	}

	content, err := os.ReadFile(absPath)
	if err != nil {
		panic(err)
	}

	strContent := strings.ReplaceAll(string(content), "\r\n", "\n")
	*lines = strings.Split(strContent, "\n")
}

func GetLinesUrl(lines *[]string, url string) {
	res, err := http.Get(url)
	if err != nil {
		panic("Error with retrieving input URL")
	}
	defer res.Body.Close()

	content, err := io.ReadAll(res.Body)
	if err != nil {
		panic("Error reading URL response body")
	}

	strContent := strings.ReplaceAll(string(content), "\r\n", "\n")
	*lines = strings.Split(strContent, "\n")
}

func CopyClipboard(toCopy string) {
	err := clipboard.Init()
	if err != nil {
		fmt.Println("Unable to copy to clipboard")
		return
	}

	clipboard.Write(clipboard.FmtText, []byte(toCopy))
	fmt.Printf("%s copied to clipboard", toCopy)
}
