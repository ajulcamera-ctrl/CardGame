# 🃏 Card Game Bot – Deployment Guide

A Telegram top-trumps-style card game bot designed to run in a Docker container on a Raspberry Pi (or any Linux machine).

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Get a Telegram Bot Token](#2-get-a-telegram-bot-token)
3. [Clone the Repository](#3-clone-the-repository)
4. [Configure the Environment](#4-configure-the-environment)
5. [Build and Run with Docker Compose](#5-build-and-run-with-docker-compose)
6. [Test the Bot in Telegram](#6-test-the-bot-in-telegram)
7. [Viewing Logs](#7-viewing-logs)
8. [Stopping and Restarting](#8-stopping-and-restarting)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Prerequisites

### Raspberry Pi OS (or any Debian-based Linux)

Update the system first:

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### Install Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

Verify Docker is running:

```bash
docker --version
```

### Install Docker Compose

Docker Compose v2 is included with Docker Desktop, but on a Raspberry Pi you may need to install the plugin manually:

```bash
sudo apt-get install -y docker-compose-plugin
```

Verify:

```bash
docker compose version
```

> **Note for older Raspberry Pi models (32-bit OS):** use `docker-compose` (v1) if the plugin is unavailable:
> ```bash
> sudo pip3 install docker-compose
> ```
> Then substitute `docker-compose` wherever `docker compose` is used below.

---

## 2. Get a Telegram Bot Token

1. Open Telegram and search for **@BotFather**.
2. Start a chat and send `/newbot`.
3. Follow the prompts:
   - Enter a **display name** (e.g. `My Card Game Bot`).
   - Enter a **username** ending in `bot` (e.g. `mycardgame_bot`).
4. BotFather will reply with a token that looks like:
   ```
   123456789:ABCdefGhIJKlmNoPQRstuVWXyz
   ```
5. **Keep this token secret** – anyone who has it can control your bot.

---

## 3. Clone the Repository

```bash
git clone https://github.com/ajulcamera-ctrl/CardGame.git
cd CardGame
```

---

## 4. Configure the Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` in a text editor:

```bash
nano .env
```

Replace the placeholder with your real token:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz
```

Save and close (`Ctrl+O`, `Enter`, `Ctrl+X` in nano).

> **Security tip:** The `.env` file is listed in `.gitignore` and will never be committed to the repository.

---

## 5. Build and Run with Docker Compose

### Build the image and start the bot

```bash
docker compose up -d --build
```

- `--build` forces Docker to rebuild the image (required the first time, or after code changes).
- `-d` runs the container in the background (detached mode).

### Confirm the container is running

```bash
docker compose ps
```

You should see the `cardgame` service listed with status `Up`.

---

## 6. Test the Bot in Telegram

1. Search for your bot by its username in Telegram.
2. Send `/start` – the bot should reply with a list of commands.
3. Start a game in a group chat or direct message:
   ```
   /newgame animals
   ```
4. Have other players join with `/join`.
5. The creator starts the round with `/gamestart`.
6. The active player taps a category button to compare cards.

### Available Packs

| Command                    | Description                        |
|----------------------------|------------------------------------|
| `/newgame animals`         | Animals with speed, strength, etc. |
| `/newgame movies`          | Movies with budget, box office, etc.|
| `/newgame countries`       | Countries with area, GDP, etc.     |
| `/newgame technology`      | Tech companies with revenue, etc.  |

### All Bot Commands

| Command          | Description                              |
|------------------|------------------------------------------|
| `/start`         | Show welcome message and command list    |
| `/newgame <pack>`| Create a new game with the chosen pack   |
| `/join`          | Join the current game in this chat       |
| `/gamestart`     | Start the game (creator only)            |
| `/status`        | Show current game status and card counts |
| `/quit`          | Leave the current game                   |

---

## 7. Viewing Logs

### Follow live logs

```bash
docker compose logs -f
```

Press `Ctrl+C` to stop following.

### Show the last 50 lines

```bash
docker compose logs --tail 50
```

---

## 8. Stopping and Restarting

### Stop the bot (container remains)

```bash
docker compose stop
```

### Start it again

```bash
docker compose start
```

### Restart the bot (e.g. after editing `.env`)

```bash
docker compose restart
```

### Stop and remove the container entirely

```bash
docker compose down
```

### Rebuild and redeploy after a code update

```bash
git pull
docker compose up -d --build
```

---

## 9. Troubleshooting

### Bot does not respond in Telegram

1. Check that the container is running:
   ```bash
   docker compose ps
   ```
2. Check the logs for errors:
   ```bash
   docker compose logs --tail 50
   ```
3. Verify your token in `.env` is correct and has no extra spaces or newlines.

### `TELEGRAM_BOT_TOKEN is not set` error in logs

The bot cannot read the token. Make sure:
- The `.env` file exists in the project directory.
- The file contains exactly `TELEGRAM_BOT_TOKEN=<your_token>` (no quotes needed).
- You restarted the container after editing `.env`:
  ```bash
  docker compose restart
  ```

### Container exits immediately

Run in the foreground to see the full error output:

```bash
docker compose up
```

Common causes: missing `.env` file, invalid token, or network connectivity issues.

### `docker compose` command not found

Try the older syntax:

```bash
docker-compose up -d --build
```

Or install the Compose plugin:

```bash
sudo apt-get install -y docker-compose-plugin
```

### Permission denied when running Docker

Add your user to the `docker` group and log out/in:

```bash
sudo usermod -aG docker $USER
```

Then either reboot or run `newgrp docker`.

### Port conflicts

This bot uses Telegram's polling API and does not expose any ports, so port conflicts are not applicable.

### Rebuilding after dependency changes

If `requirements.txt` changes, force a full rebuild:

```bash
docker compose build --no-cache
docker compose up -d
```

---

## Running Without Docker (Local Development)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your token
python main.py
```