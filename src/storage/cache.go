package storage

import (
	"context"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

const PENDING string = "pending"

type Cache struct {
	client *redis.Client
	ttl    time.Duration
}

func NewCache(redisUrl string, ttl time.Duration) *Cache {
	opt, err := redis.ParseURL(redisUrl)
	if err != nil {
		log.Fatalln("failed init redis", err)
	}

	return &Cache{
		client: redis.NewClient(opt),
		ttl:    ttl,
	}
}

func (c *Cache) GetFileId(id string) string {
	return c.client.Get(context.Background(), id).Val()
}

func (c *Cache) SetFileId(youtubeId string, fileId string) error {
	return c.client.Set(context.Background(), youtubeId, fileId, c.ttl).Err()
}

func (c *Cache) SetPending(id string) error {
	return c.client.Set(context.Background(), id, PENDING, c.ttl).Err()
}

func (c *Cache) IsPending(id string) bool {
	return c.client.Get(context.Background(), id).Val() == PENDING
}
