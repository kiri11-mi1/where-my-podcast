build:
	docker build --platform linux/amd64 -t kiri11mi1/audio_bot:latest .

push:
	docker push kiri11mi1/audio_bot:latest
