package youtube

import "errors"

var ErrInvalidYoutubeLink = errors.New("InvalidLink")
var ErrVideoDownloadFailed = errors.New("VideoDownloadFailed")
var ErrFetchingVideoInfoFailed = errors.New("FetchingVideoInfoFailed")
var ErrParseHTMLFailed = errors.New("ParseHTMLFailed")
var ErrChannelNotFound = errors.New("ChannelNotFound")