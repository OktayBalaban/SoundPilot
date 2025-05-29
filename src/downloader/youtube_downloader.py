import yt_dlp
import os
import shutil

def download_audio(youtube_url, output_folder="temp", keep_original_name=False):
    os.makedirs(output_folder, exist_ok=True)
    title = None

    def hook(d):
        nonlocal title
        if d['status'] == 'finished':
            title = d['info_dict']['title']

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [hook],
        'quiet': False,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    if not title:
        raise RuntimeError("Başlık alınamadı.")
    
    original_path = os.path.join(output_folder, f"{title}.mp3")
    if keep_original_name:
        return original_path, title
    else:
        temp_path = os.path.join(output_folder, "temp_song.mp3")
        shutil.move(original_path, temp_path)
        return temp_path, title

