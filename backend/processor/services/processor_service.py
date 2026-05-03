import tempfile
import os
import uuid
from typing import List, Dict


class ProcessorService:
    def __init__(self, runner, storage, downloader=None):
        self.runner = runner
        self.storage = storage
        self.downloader = downloader

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

    def process_url(self, url: str, stems: List[str]) -> Dict:
        if not url:
            raise ValueError("URL cannot be empty")
        if not self.downloader:
            raise RuntimeError("No downloader configured")

        title = self.downloader.extract_title(url)
        temp_path = self.downloader.download(url)

        try:
            with open(temp_path, "rb") as f:
                contents = f.read()

            processed_data = self.process_audio_file(contents, stems)
            saved_result = self.save_results(processed_data, title=title)

            # Save metadata
            self.storage.save_metadata(saved_result["job_id"], title, url)

            return saved_result
        finally:
            self._safe_remove(temp_path)
            parent = os.path.dirname(temp_path)
            if os.path.exists(parent) and not os.listdir(parent):
                os.rmdir(parent)

    def save_results(self, processed_data: Dict[str, bytes], title: str = None) -> Dict:
        job_id = title if title else str(uuid.uuid4())
        # Dosya sistemi için güvenli karakter
        job_id = "".join(c for c in job_id if c.isalnum() or c in (' ', '-', '_')).strip()

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