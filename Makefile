build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

run:
	make down
	make build
	make up
