import tempfile
import os
import uuid
from typing import List, Dict

class ProcessorService:
    def __init__(self, runner, storage):
        self.runner = runner
        self.storage = storage

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

    def save_results(self, processed_data: Dict[str, bytes]) -> Dict:
        job_id = str(uuid.uuid4())
        urls = []
        
        for stem_name, audio_bytes in processed_data.items():
            url = self.storage.save_result(job_id, stem_name, audio_bytes)
            urls.append(url)
            
        return {
            "job_id": job_id,
            "paths": urls
        }

    def _create_temp_file(self, contents: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(contents)
            return temp_file.name

    def _safe_remove(self, path: str):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    def cleanup_job(self, job_id: str):
        self.storage.delete_job(job_id)