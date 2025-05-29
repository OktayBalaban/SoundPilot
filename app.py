import gradio as gr
import os
from src.downloader.youtube_downloader import download_audio
from src.extractor.extractor import extract_stems
from src.mixer.mixer import mix_stems
from src.youtube_searcher.youtube_searcher import search_youtube_link
from dotenv import load_dotenv

load_dotenv()

def is_youtube_url(text):
    return "youtube.com/watch" in text or "youtu.be/" in text

def process_song(user_input, selected_stems):
    try:
        if is_youtube_url(user_input):
            youtube_url = user_input.strip()
        else:
            youtube_url = search_youtube_link(user_input)

        all_stems = {"vocals", "drums", "bass", "guitar (and others)"}
        keep_original = set(selected_stems) == all_stems

        mp3_path, song_title = download_audio(
            youtube_url,
            output_folder="temp",
            keep_original_name=keep_original
        )

        if keep_original:
            return os.path.abspath(mp3_path), os.path.abspath(mp3_path)

        extract_stems(mp3_path, output_folder="temp/stems")
        stem_dir = os.path.join("temp", "stems", "htdemucs", "temp_song")
        output_path = os.path.join("temp", f"{song_title}_mix.mp3")
        mix_stems(stem_dir, selected_stems, output_path=output_path)

        return os.path.abspath(output_path), os.path.abspath(output_path)

    except Exception as e:
        return f"An error occurred: {e}", None

demo = gr.Interface(
    fn=process_song,
    inputs=[
        gr.Textbox(
            label="🎵 Enter Song Name or YouTube Link",
            placeholder="e.g. 'Adele Hello' or https://www.youtube.com/watch?v=..."
        ),
        gr.CheckboxGroup(
            choices=["vocals", "drums", "bass", "guitar (and others)"],
            label="🎚️ Select stems to include in the mix",
            info="Choose which isolated stems to mix together."
        )
    ],
    outputs=[
        gr.Audio(type="filepath", label="🎧 Final Mix"),
        gr.File(label="⬇️ Download MP3")
    ],
    allow_flagging="never",
    title="🎶 SoundPilot – AI Stem Mixer",
    description="""
    <div style="text-align: center; font-size: 16px; max-width: 700px; margin: 0 auto; line-height: 1.6;">
        🎧 <strong>Enter a YouTube link or just type a song name</strong><br>
        🎼 We'll find it, extract the stems, and create your custom mix.
    </div>
    """,
    theme="default",
    css="""
        .gr-button {
            font-weight: bold;
            background: #ff6600;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .gr-button:hover {
            background: #e65c00;
        }
    """
)

if __name__ == "__main__":
    demo.launch()
