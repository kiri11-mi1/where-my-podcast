package youtube

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path"
)

type Downloader struct {
	folder string
}

func NewDownloader(folderPath string) *Downloader {
	pwd, err := os.Getwd()
	if err != nil {
		log.Fatalln(err)
	}
	fullPath := path.Join(pwd, folderPath)
	if err := os.MkdirAll(fullPath, 0755); err != nil {
		log.Fatalln(err)
	}
	log.Println("init youtube-dl:", fullPath)
	return &Downloader{folder: fullPath}
}

func (d *Downloader) Download(link, video_id string) (string, error) {
	outputPath := fmt.Sprintf("%s/%s.mp3", d.folder, video_id)
	cmd := exec.Command("yt-dlp", "-x", "--audio-format", "mp3", "-o", outputPath, link)

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Run()
	if err != nil {
		return "", ErrVideoDownloadFailed
	}
	return outputPath, nil
}
