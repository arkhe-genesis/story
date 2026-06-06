package main

import (
	"fmt"
	"regexp"
)

func main() {
    descRegex := regexp.MustCompile(`^[a-zA-Z0-9 .&/-]+$`) // e.g. "add foo-bar"
    fmt.Println(descRegex.MatchString("Add Auto-Canonization Engine (Substrato 1079 & 1080)"))
}
