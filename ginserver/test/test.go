package main

import (
	"fmt"

	"github.com/sergi/go-diff/diffmatchpatch"
)

const (
	text1 = "hello w Lorem ipsum dolor. asdfasfas"
	text2 = "hello world Lorem dolor sit amets"
)

func update(text1 string, text2 string) (string, []bool) {
	dmp := diffmatchpatch.New()

	diffs := dmp.DiffMain(text1, text2, false)

	patchs := dmp.PatchMake(diffs)

	result, applied := dmp.PatchApply(patchs, text1)

	return result, applied
}

func main() {

	r, e := update(text1, text2)
	fmt.Println(r, e)

}
