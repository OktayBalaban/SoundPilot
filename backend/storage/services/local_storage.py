import os
import shutil
from core.base_storage import StorageService

class LocalStorageService(StorageService):
    def __init__(self, base_path: str, static_url_prefix: str):
        self.base_path = base_path
        self.static_url_prefix = static_url_prefix
        os.makedirs(self.base_path, exist_ok=True)

    def save_result(self, job_id: str, stem_name: str, data: bytes) -> str:
        job_dir = os.path.join(self.base_path, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        filename = f"{stem_name}.wav"
        file_path = os.path.join(job_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(data)
            
        return f"{self.static_url_prefix}/{job_id}/{filename}"

    def delete_job(self, job_id: str):
        job_dir = os.path.join(self.base_path, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)