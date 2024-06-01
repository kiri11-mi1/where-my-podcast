FROM golang:latest as prod

RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

RUN mkdir /app
ADD src /app/
WORKDIR /app
RUN go build -o main .
CMD ["./main"]