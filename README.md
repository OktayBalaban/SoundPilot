# SoundPilot

A lightweight tool for splitting songs into stems. Paste a YouTube link or drop an audio file — get isolated vocals, drums, bass, and instruments. Mix them however you want.

![SoundPilot](screenshot.png)

## Features

- YouTube URL or file upload
- AI stem separation (vocals, drums, bass, other)
- Real-time mixer with mute, volume, and pitch shift
- Auto-saved song library

## Run

```bash
git clone https://github.com/OktayBalaban/SoundPilot.git
cd SoundPilot
docker compose up --build
```

Open `http://localhost:3000`. That's it.

NVIDIA GPU speeds things up but isn't required.

## Stack

Demucs (Meta AI) · FastAPI · SvelteKit · Tone.js · Docker