import tempfile
import os
from typing import List, Dict

class ProcessorService:
    def __init__(self, runner):
        self.runner = runner

    def process_audio_file(self, file_contents: bytes, stems: List[str]) -> Dict[str, bytes]:
        if not file_contents:
            raise ValueError("Empty file contents")
        if not stems:
            raise ValueError("At least one stem must be requested")

        temp_input_path = self._create_temp_file(file_contents)
        
        try:
            return self.runner.run(temp_input_path, stems)
        finally:
            self._safe_remove(temp_input_path)

    def _create_temp_file(self, contents: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(contents)
            return temp_file.name

    def _safe_remove(self, path: str):
        if os.path.exists(path):
            os.remove(path)