import os
import soundfile as sf
import numpy as np
from pydub import AudioSegment

def mix_stems(stem_dir, selected_stems, output_path="temp/mixed_output.mp3"):
    if not selected_stems:
        print("No stems selected.")
        return

    mix = None
    sr = None
    available_files = {file.lower(): file for file in os.listdir(stem_dir)}

    for stem in selected_stems:
        filename = f"{stem}.wav".lower()
        if filename not in available_files:
            print(f"Stem not found: {filename}")
            continue

        full_path = os.path.join(stem_dir, available_files[filename])
        print(f"Mixing: {full_path}")
        audio, sr = sf.read(full_path)

        if mix is None:
            mix = audio
        else:
            min_len = min(len(mix), len(audio))
            mix = mix[:min_len] + audio[:min_len]

    if mix is not None:
        temp_wav_path = output_path.replace(".mp3", "_temp.wav")
        sf.write(temp_wav_path, mix, sr, format="WAV", subtype="PCM_16")

        sound = AudioSegment.from_wav(temp_wav_path)
        sound.export(output_path, format="mp3", bitrate="192k")

        os.remove(temp_wav_path)

        print(f"✅ Mixed MP3 saved at: {output_path}")
    else:
        print("❌ Mixing failed: No valid stems found.")
