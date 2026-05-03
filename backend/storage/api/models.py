from pydantic import BaseModel
from typing import List, Dict, Optional


class UploadResponse(BaseModel):
    url: str


class DeleteResponse(BaseModel):
    status: str


class SongEntry(BaseModel):
    id: str
    title: str
    source_url: str = ""
    created_at: str = ""
    is_valid: bool = True
    missing_stems: List[str] = []
    stems: Dict[str, str] = {}


class LibraryResponse(BaseModel):
    songs: List[SongEntry]
    total: int


class MetadataRequest(BaseModel):
    title: str
    source_url: str = ""