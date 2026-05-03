import pytest
import os
import json
from services.local_library import LocalLibraryService
from core.stem_validator import StemValidator
from core.metadata_service import MetadataService


@pytest.fixture
def library_setup(tmp_path):
    base = tmp_path / "data"
    base.mkdir()
    validator = StemValidator()
    metadata = MetadataService()
    service = LocalLibraryService(str(base), "/files", validator, metadata)
    return service, base, metadata


def _create_valid_song(base, name, metadata_svc=None, title=None, url=""):
    song_dir = base / name
    song_dir.mkdir()
    for stem in ["vocals.wav", "drums.wav", "bass.wav", "other.wav"]:
        (song_dir / stem).write_bytes(b"fake-audio")
    if metadata_svc and title:
        metadata_svc.write(str(song_dir), title, url)
    return song_dir


def test_list_songs_returns_valid_entries(library_setup):
    service, base, meta = library_setup
    _create_valid_song(base, "song-1", meta, "My Song")
    _create_valid_song(base, "song-2", meta, "Another Song")

    songs = service.list_songs()
    assert len(songs) == 2
    assert songs[0].title == "My Song"       # song-1 alphabetically first
    assert songs[1].title == "Another Song"   # song-2 second


def test_list_songs_empty_library(library_setup):
    service, _, _ = library_setup
    assert service.list_songs() == []


def test_get_song_returns_entry(library_setup):
    service, base, meta = library_setup
    _create_valid_song(base, "test-song", meta, "Test Song", "https://youtube.com/123")

    song = service.get_song("test-song")
    assert song is not None
    assert song.title == "Test Song"
    assert song.source_url == "https://youtube.com/123"
    assert song.is_valid is True
    assert "vocals" in song.stems


def test_get_song_not_found(library_setup):
    service, _, _ = library_setup
    assert service.get_song("nonexistent") is None


def test_get_song_with_missing_stems(library_setup):
    service, base, _ = library_setup
    song_dir = base / "broken-song"
    song_dir.mkdir()
    (song_dir / "vocals.wav").write_bytes(b"data")

    song = service.get_song("broken-song")
    assert song.is_valid is False
    assert len(song.missing_stems) == 3


def test_delete_song_removes_directory(library_setup):
    service, base, meta = library_setup
    _create_valid_song(base, "to-delete", meta, "Delete Me")

    assert service.delete_song("to-delete") is True
    assert not (base / "to-delete").exists()


def test_delete_nonexistent_song(library_setup):
    service, _, _ = library_setup
    assert service.delete_song("ghost") is False


def test_song_without_metadata_uses_folder_name(library_setup):
    service, base, _ = library_setup
    _create_valid_song(base, "no-meta-song")

    song = service.get_song("no-meta-song")
    assert song.title == "no-meta-song"