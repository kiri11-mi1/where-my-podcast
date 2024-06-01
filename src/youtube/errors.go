package youtube

import "errors"

var ErrInvalidYoutubeLink = errors.New("InvalidLink")
var ErrVideoDownloadFailed = errors.New("VideoDownloadFailed")