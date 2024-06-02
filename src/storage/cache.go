package storage

import (
	"context"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

type Cache struct {
	client *redis.Client
	ttl    time.Duration
}

func NewCache(redisUrl string, ttl time.Duration) *Cache {
	log.Println("init redis:", redisUrl)
	opt, err := redis.ParseURL(redisUrl)
	if err != nil {
		log.Fatalln("failed init redis", err)
	}

	return &Cache{
		client: redis.NewClient(opt),
		ttl:    ttl,
	}
}

func (c *Cache) Get(id string) string {
	return c.client.Get(context.Background(), id).Val()
}

func (c *Cache) Set(youtubeId string, fileId string) error {
	return c.client.Set(context.Background(), youtubeId, fileId, c.ttl).Err()
}
