import subprocess
import os

def extract_stems(audio_path, output_folder="temp/stems"):
    os.makedirs(output_folder, exist_ok=True)

    result = subprocess.run([
        "demucs",
        "--out", output_folder,
        audio_path
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Extraction failed:\n", result.stderr)
    else:
        print("Extraction completed.")
