import pytest
from core.stem_validator import StemValidator


@pytest.fixture
def validator():
    return StemValidator()


def test_valid_song_directory(validator, tmp_path):
    for stem in ["vocals.wav", "drums.wav", "bass.wav", "other.wav"]:
        (tmp_path / stem).write_bytes(b"data")
    assert validator.is_valid(str(tmp_path)) is True


def test_missing_stems(validator, tmp_path):
    (tmp_path / "vocals.wav").write_bytes(b"data")
    assert validator.is_valid(str(tmp_path)) is False
    missing = validator.get_missing_stems(str(tmp_path))
    assert "drums.wav" in missing
    assert "bass.wav" in missing
    assert "other.wav" in missing


def test_nonexistent_directory(validator):
    assert validator.is_valid("/nonexistent/path") is False


def test_empty_directory(validator, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert validator.is_valid(str(empty)) is False
    assert len(validator.get_missing_stems(str(empty))) == 4