import json
import os
from datetime import datetime, timezone
from typing import Optional


class MetadataService:
    """Handles reading and writing song metadata."""

    FILENAME = "metadata.json"

    def write(self, song_dir: str, title: str, source_url: str = "") -> dict:
        metadata = {
            "title": title,
            "source_url": source_url,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        path = os.path.join(song_dir, self.FILENAME)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return metadata

    def read(self, song_dir: str) -> Optional[dict]:
        path = os.path.join(song_dir, self.FILENAME)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)