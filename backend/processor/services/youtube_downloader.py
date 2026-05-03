import tempfile
import os
import glob
import yt_dlp


class YouTubeDownloader:
    """Downloads audio from a YouTube URL as a WAV file."""

    def download(self, url: str) -> str:
        temp_dir = tempfile.mkdtemp(prefix="soundpilot_")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'outtmpl': os.path.join(temp_dir, "source.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        wav_files = glob.glob(os.path.join(temp_dir, "*.wav"))

        if not wav_files:
            raise FileNotFoundError(f"Download failed: no wav file in {temp_dir}")

        return wav_files[0]

    def extract_title(self, url: str) -> str:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Unknown')