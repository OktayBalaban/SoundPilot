from abc import ABC, abstractmethod
from typing import Dict

class AudioRunner(ABC):
    @abstractmethod
    def run(self, file_path: str, settings: Dict) -> Dict[str, bytes]:
        pass