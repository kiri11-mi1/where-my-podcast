package test_youtube

import (
	"testing"
	"where-my-podcast/youtube"

	"github.com/stretchr/testify/assert"
)

func TestUtils_IsValidLink(t *testing.T) {
	t.Run("link is valid", func(t *testing.T) {
		link := "https://www.youtube.com/watch?v=v6rMPOlPzpy"
		actual := youtube.IsValidLink(link)
		assert.Equal(t, true, actual)
	})
	t.Run("link is not valid", func(t *testing.T) {
		link := "https://www.youtube.com/watch?v=invalid_id"
		actual := youtube.IsValidLink(link)
		assert.Equal(t, false, actual)
	})
	t.Run("link is valid", func(t *testing.T) {
		link := "https://youtu.be/GGq0BIF0GXc?si=2jXbI4H_JkqA2tiB"
		actual := youtube.IsValidLink(link)
		assert.Equal(t, true, actual)
	})
	t.Run("link is not valid", func(t *testing.T) {
		link := "https://www.youtube.com/embed/dQw4w9WgXcQ"
		actual := youtube.IsValidLink(link)
		assert.Equal(t, false, actual)
	})
}

func TestUtils_Link2Id(t *testing.T) {
	t.Run("success fetch id", func(t *testing.T) {
		link := "https://www.youtube.com/watch?v=v6rMPOlPzpy"
		expected := "v6rMPOlPzpy"
		actual, err := youtube.Link2Id(link)
		assert.NoError(t, err)
		assert.Equal(t, expected, actual)
	})
	t.Run("success fetch id", func(t *testing.T) {
		link := "https://youtu.be/GGq0BIF0GXc?si=2jXbI4H_JkqA2tiB"
		expected := "GGq0BIF0GXc"
		actual, err := youtube.Link2Id(link)
		assert.NoError(t, err)
		assert.Equal(t, expected, actual)
	})
	t.Run("fail fetch id", func(t *testing.T) {
		link := "https://www.youtube.com/embed/dQw4w9WgXcQ"
		_, err := youtube.Link2Id(link)
		assert.ErrorIs(t, err, youtube.ErrInvalidYoutubeLink)
	})
}
