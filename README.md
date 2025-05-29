# 🎶 SoundPilot – AI Stem Mixer from YouTube

SoundPilot lets you extract and remix vocals, drums, bass, or other stems from songs using just a YouTube link or song name.

## ⚙️ Setup

```
git clone https://github.com/your-username/soundpilot.git
cd soundpilot
python -m venv venv
venv\Scripts\activate   # or: source venv/bin/activate
pip install -r requirements.txt
```

Then add your Gemini key to a `.env` file:

```
GEMINI_API_KEY=your-gemini-key
```

---

## ▶️ Run

```
python main.py
```

Then go to: http://localhost:7860

---

## 📦 Requirements

```
yt-dlp
demucs
soundfile
gradio
pydub
python-dotenv
duckduckgo_search>=0.9.4
```

---

## 🛡 License

MIT – use freely, credit appreciated!
