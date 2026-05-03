from abc import ABC, abstractmethod
from typing import Dict

class StorageService(ABC):
    @abstractmethod
    def save_result(self, job_id: str, stem_name: str, data: bytes) -> str:
        """Saves the processed stem and returns its access URL or path."""
        pass

    @abstractmethod
    def delete_job(self, job_id: str):
        """Removes all files associated with a specific job."""
        pass