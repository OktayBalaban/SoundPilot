import subprocess
import os
import shutil
import tempfile
from typing import Dict, List
from services.base_runner import AudioRunner
from api.config import settings

class DemucsRunner(AudioRunner):
    def __init__(self, model_name: str, default_stems: str):
        self.model_name = model_name
        self.default_stems = default_stems

    def run(self, file_path: str, stems: List[str] = None) -> Dict[str, bytes]:
        target_stems = stems if stems else [self.default_stems]
        output_dir = tempfile.mkdtemp()
        
        try:
            self._execute_demucs(file_path, output_dir, target_stems)
            
            model_path = self._get_model_output_path(output_dir, file_path)
            
            return self._collect_stems(model_path, target_stems)
            
        finally:
            self._cleanup(output_dir)

    def _execute_demucs(self, file_path: str, output_dir: str, stems: List[str]):
        command = ["demucs", "-n", settings.demucs_model, "-o", output_dir, file_path]
        if len(stems) == 1:
            command.extend(["--two-stems", stems[0]])
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            full_error = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            print(f"--- DEMUCS FAILED ---\n{full_error}")
            raise RuntimeError(f"Demucs CLI Error: {full_error}")

    def _get_model_output_path(self, output_dir: str, file_path: str) -> str:
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
        path = os.path.join(output_dir, settings.demucs_model, base_filename)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Expected output directory not found: {path}")
        return path

    def _collect_stems(self, model_path: str, target_stems: List[str]) -> Dict[str, bytes]:
        if len(target_stems) > 1:
            return self._fetch_requested_stems(model_path, target_stems)
        return self._fetch_all_available_stems(model_path)

    def _fetch_requested_stems(self, model_path: str, stems: List[str]) -> Dict[str, bytes]:
        results = {}
        for stem in stems:
            path = os.path.join(model_path, f"{stem}.wav")
            if os.path.exists(path):
                results[stem] = self._read_binary(path)
        return results

    def _fetch_all_available_stems(self, model_path: str) -> Dict[str, bytes]:
        return {
            os.path.splitext(f)[0]: self._read_binary(os.path.join(model_path, f))
            for f in os.listdir(model_path) if f.endswith(".wav")
        }

    def _read_binary(self, path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def _cleanup(self, path: str):
        if os.path.exists(path):
            shutil.rmtree(path)