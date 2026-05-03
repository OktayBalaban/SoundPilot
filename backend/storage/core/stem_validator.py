import os
from typing import List

REQUIRED_STEMS = {"vocals.wav", "drums.wav", "bass.wav", "other.wav"}


class StemValidator:
    """Validates that a song directory contains all required stem files."""

    def __init__(self, required_stems: set = None):
        self.required_stems = required_stems or REQUIRED_STEMS

    def is_valid(self, song_dir: str) -> bool:
        if not os.path.isdir(song_dir):
            return False
        files = set(os.listdir(song_dir))
        return self.required_stems.issubset(files)

    def get_missing_stems(self, song_dir: str) -> List[str]:
        if not os.path.isdir(song_dir):
            return list(self.required_stems)
        files = set(os.listdir(song_dir))
        return sorted(self.required_stems - files)