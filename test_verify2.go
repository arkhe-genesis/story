package main

import (
	"fmt"
	"regexp"
)

func main() {
	descRegex := regexp.MustCompile(`^[a-zA-Z0-9 .&/-]+$`)
	fmt.Println(descRegex.MatchString("add Moltbook Identity Bridge"))
}
