import httpx
from .base_storage import StorageService

class RemoteStorageService(StorageService):
    def __init__(self, endpoint: str = "http://localhost:8001"):
        self.endpoint = endpoint

    def save_result(self, job_id: str, stem_name: str, data: bytes) -> str:
        files = {'file': (f"{stem_name}.wav", data)}
        params = {"stem_name": stem_name}
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.endpoint}/upload/{job_id}",
                files=files,
                params=params
            )
            response.raise_for_status()
            return response.json()["url"]
    
    def save_metadata(self, job_id: str, title: str, source_url: str = ""):
        with httpx.Client() as client:
            response = client.post(
                f"{self.endpoint}/library/{job_id}/metadata",
                json={"title": title, "source_url": source_url}
            )
            response.raise_for_status()

    def delete_job(self, job_id: str):
        with httpx.Client() as client:
            client.delete(f"{self.endpoint}/jobs/{job_id}")