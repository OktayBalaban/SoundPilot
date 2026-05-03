from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def save_result(self, job_id: str, stem_name: str, data: bytes) -> str:
        pass

    @abstractmethod
    def delete_job(self, job_id: str):
        pass

    @abstractmethod
    def save_metadata(self, job_id: str, title: str, source_url: str = ""):
        pass