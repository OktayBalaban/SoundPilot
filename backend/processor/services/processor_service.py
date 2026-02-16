import tempfile
import os
import uuid
import shutil
from typing import List, Dict

# Çıktıların ana dizini (backend/outputs)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

class ProcessorService:
    def __init__(self, runner):
        self.runner = runner
        os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        job_dir = os.path.join(OUTPUT_DIR, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        file_urls = []
        
        for stem_name, audio_bytes in processed_data.items():
            filename = f"{stem_name}.wav"
            file_path = os.path.join(job_dir, filename)
            
            with open(file_path, "wb") as f:
                f.write(audio_bytes)
            
            web_url = f"/static/{job_id}/{filename}"
            file_urls.append(web_url)
            
        return {
            "job_id": job_id,
            "paths": file_urls
        }

    def _create_temp_file(self, contents: bytes) -> str:
        """Geçici bir .wav dosyası oluşturur ve yolunu döner."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(contents)
            return temp_file.name

    def _safe_remove(self, path: str):
        """Dosyayı güvenli bir şekilde siler."""
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Dosya silme hatası: {path} - {e}")

    def cleanup_job(self, job_id: str):
        """
        İsteğe bağlı: Belirli bir işlemi diskten tamamen temizlemek için kullanılır.
        """
        job_dir = os.path.join(OUTPUT_DIR, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)