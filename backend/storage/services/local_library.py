import os
import shutil
from typing import List, Optional
from core.base_library import LibraryService
from core.stem_validator import StemValidator
from core.metadata_service import MetadataService
from api.models import SongEntry


class LocalLibraryService(LibraryService):
    def __init__(self, base_path: str, static_url_prefix: str,
                 validator: StemValidator, metadata: MetadataService):
        self.base_path = base_path
        self.static_url_prefix = static_url_prefix
        self.validator = validator
        self.metadata = metadata

    def list_songs(self) -> List[SongEntry]:
        songs = []
        if not os.path.exists(self.base_path):
            return songs

        for name in sorted(os.listdir(self.base_path)):
            song_dir = os.path.join(self.base_path, name)
            if not os.path.isdir(song_dir):
                continue

            entry = self._build_entry(name, song_dir)
            songs.append(entry)

        return songs

    def get_song(self, song_id: str) -> Optional[SongEntry]:
        song_dir = os.path.join(self.base_path, song_id)
        if not os.path.isdir(song_dir):
            return None
        return self._build_entry(song_id, song_dir)

    def delete_song(self, song_id: str) -> bool:
        song_dir = os.path.join(self.base_path, song_id)
        if not os.path.exists(song_dir):
            return False
        shutil.rmtree(song_dir)
        return True

    def _build_entry(self, song_id: str, song_dir: str) -> SongEntry:
        meta = self.metadata.read(song_dir)
        is_valid = self.validator.is_valid(song_dir)
        missing = self.validator.get_missing_stems(song_dir) if not is_valid else []

        stems = {}
        for f in os.listdir(song_dir):
            if f.endswith(".wav"):
                stem_name = f.replace(".wav", "")
                stems[stem_name] = f"{self.static_url_prefix}/{song_id}/{f}"

        return SongEntry(
            id=song_id,
            title=meta.get("title", song_id) if meta else song_id,
            source_url=meta.get("source_url", "") if meta else "",
            created_at=meta.get("created_at", "") if meta else "",
            is_valid=is_valid,
            missing_stems=missing,
            stems=stems
        )