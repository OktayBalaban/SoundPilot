Overview
-
This folder contains a small FastAPI processor that uses Demucs to separate audio
into stems and then mixes selected stems into a single WAV.

Files
- `main.py`: FastAPI app entry (POST /process)
- `processor/`: service and demucs wrapper
- `utils/audio_utils.py`: lightweight mixing utilities (wave + numpy)
- `tests/`: pytest unit tests (uses `FakeDemucsRunner`)

Run
- Install requirements from `requirements.txt` (Demucs and its deps may be heavy).

Example run (development):
```
pip install -r requirements.txt
uvicorn processor.main:app --reload --port 8000
```

Notes
- `RealDemucsRunner` expects a working `demucs` command in PATH. For unit tests,
  the `FakeDemucsRunner` produces small silent WAV files.
