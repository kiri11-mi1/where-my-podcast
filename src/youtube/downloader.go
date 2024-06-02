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
	pwd, _ := os.Getwd()
	log.Println("init youtube-dl:", path.Join(pwd, folderPath))
	return &Downloader{folder: folderPath}
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
