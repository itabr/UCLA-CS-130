package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/sergi/go-diff/diffmatchpatch"
	"gopkg.in/olahol/melody.v1"
)

func update(text1 string, text2 string) (string, []bool) {
	dmp := diffmatchpatch.New()

	diffs := dmp.DiffMain(text1, text2, false)

	patchs := dmp.PatchMake(diffs)

	result, applied := dmp.PatchApply(patchs, text1)

	return result, applied
}

// main function
func main() {

	r := gin.Default()

	r.Static("/assets", "./assets")

	r.LoadHTMLGlob("templates/*")

	m := melody.New()

	r.GET("/", GetHomePage)

	r.GET("/create", Create)

	r.GET("/ajax", Ajax)

	r.GET("/workplace/:key", Workplace)

	r.GET("/ws", func(c *gin.Context) {

		m.HandleRequest(c.Writer, c.Request)
	})

	m.HandleMessage(func(s *melody.Session, msg []byte) {

		f, err := os.OpenFile("workplaces/test", os.O_RDWR, 0755)
		if err != nil {
			log.Fatal(err)
		}
		FileInfo, err := f.Stat()
		if err != nil {
			log.Fatal(err)
		}

		b := make([]byte, FileInfo.Size())
		f.Read(b)

		dmp := diffmatchpatch.New()
		diffs := dmp.DiffMain(string(b), string(msg), false)
		patchs := dmp.PatchMake(diffs)
		data, err := json.Marshal(&patchs)
		if err != nil {
			fmt.Println(err)
			return
		}

		result, applied := dmp.PatchApply(patchs, string(b))
		fmt.Println(result, applied)
		fmt.Println(string(data))

		ioutil.WriteFile("workplaces/test", []byte(result), 0644)
		m.BroadcastOthers([]byte(data), s)
		// m.Broadcast(data)

	})

	r.Run(":8080")
}

type Problem struct {
	Stmt string
	Tag  string
}

//  /
func GetHomePage(c *gin.Context) {
	c.HTML(http.StatusOK, "index.tmpl", gin.H{
		"title": "Main page",
	})
}

// /create
func Create(c *gin.Context) {
	// TODO
	key := "test"
	c.Redirect(http.StatusMovedPermanently, "/workplace/"+key)
}

// /ajax
func Ajax(c *gin.Context) {
	var p Problem
	q := c.Request.URL.Query()
	p.Stmt = q["Smt"][0]
	if p.Stmt != "" {
		// TODO
		p.Tag = string("some tag")
		c.JSON(http.StatusOK, gin.H{"status": "StatusOK", "Tag": p.Tag})
	} else {
		c.JSON(http.StatusNoContent, gin.H{"status": "StatusOK", "Tag": ""})
	}
}

// /workplace/:key
func Workplace(c *gin.Context) {
	key := c.Param("key")

	f, err := os.OpenFile("workplaces/"+key, os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		log.Fatal(err)
	}

	FileInfo, err := f.Stat()
	if err != nil {
		log.Fatal(err)
	}

	b := make([]byte, FileInfo.Size())
	f.Read(b)

	c.HTML(http.StatusOK, "wp.tmpl", gin.H{
		"title": "workplace page",
		"data":  string(b),
	})
}
