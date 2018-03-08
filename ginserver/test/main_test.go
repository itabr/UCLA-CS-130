package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSomething(t *testing.T) {

	assert.True(t, true, "True is true!")

	a := "hello w Lorem ipsum dolor."
	b := "hello world Lorem dolor sit amets"

	result, e := update(a, b)
	_ = e
	assert.True(t, result == "hello world Lorem dolor sit amets", "True is true!")

	a = ""
	b = ""
	result, e = update(a, b)
	assert.True(t, result == "", "True is true!")

	a = "1"
	b = "2"
	result, e = update(a, b)
	assert.True(t, result == "2", "True is true!")

	a = "hello"
	b = "hi"
	result, e = update(a, b)
	assert.True(t, result == "hi", "True is true!")

	a = "hello world"
	b = ""
	result, e = update(a, b)
	assert.True(t, result == "", "True is true!")

	a = ""
	b = "hello world Lorem dolor sit amets"
	result, e = update(a, b)
	assert.True(t, result == "hello world Lorem dolor sit amets", "True is true!")

	a = "hello "
	b = "      world"
	result, e = update(a, b)

	assert.True(t, result != "hello world", "True is true!")

}
