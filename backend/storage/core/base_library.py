from abc import ABC, abstractmethod
from typing import List, Optional
from api.models import SongEntry


class LibraryService(ABC):
    @abstractmethod
    def list_songs(self) -> List[SongEntry]:
        pass

    @abstractmethod
    def get_song(self, song_id: str) -> Optional[SongEntry]:
        pass

    @abstractmethod
    def delete_song(self, song_id: str) -> bool:
        pass