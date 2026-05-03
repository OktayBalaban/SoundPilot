# SoundPilot

A local tool for splitting songs into stems. Drop an audio file or paste a YouTube link — get isolated vocals, drums, bass, and instruments. Mix them in real time.

Built as a personal utility. Not intended for deployment — YouTube integration alone makes public hosting impractical, and there's no real need for it beyond local use.

![SoundPilot](screenshot.png)

## Features

- YouTube URL or local file upload
- AI-powered stem separation (vocals, drums, bass, other)
- Real-time mixer — per-stem volume, mute, and pitch shift
- Persistent song library with metadata
- Bilingual UI (English / Turkish)

## Architecture

Three independently containerized services, each with its own responsibility and test suite:

```
┌────────────┐       ┌──────────────────┐       ┌─────────────────┐
│  Frontend   │──────▶│    Processor      │──────▶│    Storage       │
│  SvelteKit  │ :3000 │    FastAPI        │ :8000 │    FastAPI       │ :8001
│  Tone.js    │◀──────│    Demucs (AI)    │       │    Local FS      │
└────────────┘       └──────────────────┘       └─────────────────┘
```

**Frontend** sends audio or YouTube URLs to the Processor, then plays back stems via Tone.js with real-time volume, mute, and pitch controls.

**Processor** runs Demucs for AI stem separation and uploads results to Storage. Downloads YouTube audio via yt-dlp when a URL is provided.

**Storage** persists WAV files on the local filesystem, serves them over HTTP, and manages the song library (metadata, listing, deletion).

Services communicate over HTTP. Processor and Storage are decoupled through an abstract `StorageService` interface — the Processor doesn't know (or care) whether it's writing to a local disk or a remote service.

## Run

```bash
git clone https://github.com/OktayBalaban/SoundPilot.git
cd SoundPilot
docker compose up --build
```

Open `http://localhost:3000`.

NVIDIA GPU speeds things up significantly but isn't required. For CPU-only:

```bash
docker compose -f docker-compose.yml -f docker-compose.cpu.yml up --build
```

Processing will be slower (~3-5 min per song) but fully functional.

## Stack

Demucs (Meta AI) · FastAPI · SvelteKit · Tone.js · Docker

## Design Notes

**Service separation** — Processor carries heavy ML dependencies (PyTorch, Demucs) and benefits from GPU access. Storage is a thin file server. Keeping them separate means independent scaling concerns and the ability to rebuild one without touching the other.

**Demucs (htdemucs)** — Meta's model provides strong stem separation quality with a straightforward CLI. GPU support comes out of the box, and it handles all four standard stems without additional configuration.

**Tone.js** — Synchronized multi-track playback with per-stem pitch shifting requires more than the raw Web Audio API. Tone.js gives us `PitchShift`, transport-level sync, and clean gain control without reinventing the wheel.

**Abstract base classes** — `AudioRunner` and `StorageService` are abstract interfaces. The Processor depends on these abstractions, not on concrete implementations. This keeps the service testable (mock runners in tests, real Demucs in production) and makes it straightforward to swap implementations if needed.

## Testing

```bash
./test.sh
```

Runs all three test suites (Processor, Storage, Frontend) with a single command. Tests are isolated — service tests use mocked dependencies, frontend tests cover both components and business logic.

For integration tests that run the actual Demucs model:

```bash
RUN_HEAVY=true python3 -m pytest backend/processor/tests/ -v
```