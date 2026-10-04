version: "3.9"

services:
  kenna-bot:
    build: .
    container_name: kenna-bot
    env_file:
      - .env
    volumes:
      - .:/app
    restart: unless-stopped
