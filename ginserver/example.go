package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"gopkg.in/olahol/melody.v1"
)

// main function
func main() {

	r := gin.Default()

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
		m.Broadcast(msg)
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
	c.HTML(http.StatusOK, "wp.tmpl", gin.H{
		"title": "workplace page",
	})
}
