import pytest
import os
from unittest.mock import patch, MagicMock
from services.youtube_downloader import YouTubeDownloader


@pytest.fixture
def downloader():
    return YouTubeDownloader()


def test_download_calls_ytdlp_with_correct_url(downloader):
    with patch("services.youtube_downloader.yt_dlp.YoutubeDL") as MockYDL:
        mock_instance = MagicMock()
        MockYDL.return_value.__enter__ = MagicMock(return_value=mock_instance)
        MockYDL.return_value.__exit__ = MagicMock(return_value=False)

        with patch("services.youtube_downloader.glob.glob") as mock_glob:
            mock_glob.return_value = ["/tmp/soundpilot_test/source.wav"]
            result = downloader.download("https://youtube.com/watch?v=abc123")

        mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=abc123"])
        assert result == "/tmp/soundpilot_test/source.wav"


def test_download_raises_error_when_file_not_found(downloader):
    """
    Scenario: yt-dlp runs but output file is missing.
    Expected: FileNotFoundError is raised.
    """
    with patch("services.youtube_downloader.yt_dlp.YoutubeDL") as MockYDL:
        mock_instance = MagicMock()
        MockYDL.return_value.__enter__ = MagicMock(return_value=mock_instance)
        MockYDL.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(FileNotFoundError, match="Download failed"):
            downloader.download("https://youtube.com/watch?v=invalid")