package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"encoding/json"
)

func toJson(p interface{}) string {
	bytes, err := json.Marshal(p)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}

	return string(bytes)
}

type FileContent struct {
	Info string `json:"info"`
	Playlists []Playlist `json:"playlists"`
}

type Playlist struct {
	Name string `json:"name"`
	Collaborative string `json:"collaborative"`
	Tracks []Track `json:"tracks"`
}

type Track struct {
	Pos float64 `json:"pos"`
	ArtistName string `json:"artist_name"`
	TrackName string `json:"track_name"`
	AlbumName string `json:"album_name"`
}

func main() {
	files, err := ioutil.ReadDir("E:\\D\\FRI\\mpd.v1\\data")
	if err != nil {
		log.Fatal(err)
	}

	for _, file := range files {
		fmt.Println(file.Name())
		content, err := ioutil.ReadFile("E:\\D\\FRI\\mpd.v1\\data\\" + file.Name())
		if err != nil {
			log.Fatal(err)
		}
		//fmt.Println(content)

		var playlists FileContent
		//read json
		err = json.Unmarshal(content, &playlists)
		if err != nil {
			fmt.Println("error:", err)
		}
		//fmt.Printf("%+v", playlists)

		for _, playlist := range playlists.Playlists {
			fmt.Printf("%+v", playlist.Name)
		}

		//put playlists in one list and songs in another

		break
	}
}
