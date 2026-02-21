# backend/processor/services/remote_storage.py
import httpx
from .base_storage import StorageService

class RemoteStorageService(StorageService):
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    def save_result(self, job_id: str, stem_name: str, data: bytes) -> str:
        files = {'file': (f"{stem_name}.wav", data)}
        params = {"stem_name": stem_name}
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/upload/{job_id}", 
                files=files, 
                params=params
            )
            response.raise_for_status()
            return response.json()["url"]

    def delete_job(self, job_id: str):
        with httpx.Client() as client:
            client.delete(f"{self.base_url}/jobs/{job_id}")