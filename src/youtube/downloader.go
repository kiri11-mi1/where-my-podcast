package youtube

type Downloader struct{}

func NewDownloader() *Downloader {
	return &Downloader{}
}

func (d *Downloader) Download(url string) {
	// TODO: скачивание ролика
	panic("not implemented")
}
