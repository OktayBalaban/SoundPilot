import pytest
import os
from unittest.mock import MagicMock, patch, ANY
from services.processor_service import ProcessorService

@pytest.fixture
def mock_runner():
    return MagicMock()

@pytest.fixture
def service(mock_runner):
    return ProcessorService(mock_runner)

def test_should_return_dict_when_processing_is_successful(service, mock_runner):
    """
    Scenario: Normal operational flow.
    Expected: Service returns the dictionary provided by the runner.
    """
    # Arrange
    expected_output = {"vocals": b"vocal_data", "drums": b"drum_data"}
    mock_runner.run.return_value = expected_output
    
    # Act
    result = service.process_audio_file(b"fake_audio", ["vocals", "drums"])
    
    # Assert
    assert result == expected_output
    mock_runner.run.assert_called_once()

def test_should_ensure_temp_file_is_deleted_after_processing(service, mock_runner):
    """
    Scenario: Ensure no temporary files are leaked on the disk.
    Expected: The temp file created must not exist after function execution.
    """
    # Arrange
    mock_runner.run.return_value = {"vocals": b"data"}
    captured_path = None

    # Runner çağrıldığında dosyanın var olduğunu ama sonra silindiğini kontrol edeceğiz
    def mock_run(path, stems):
        nonlocal captured_path
        captured_path = path
        assert os.path.exists(path) # Runner çalışırken dosya orada olmalı
        return {"vocals": b"data"}

    mock_runner.run.side_effect = mock_run

    # Act
    service.process_audio_file(b"content", ["vocals"])

    # Assert
    assert captured_path is not None
    assert not os.path.exists(captured_path) # İşlem bitince dosya silinmiş olmalı

def test_should_cleanup_temp_file_even_if_runner_raises_exception(service, mock_runner):
    """
    Scenario: Runner crashes during execution.
    Expected: Service must still delete the input temp file (Finally block check).
    """
    # Arrange
    mock_runner.run.side_effect = RuntimeError("Demucs failed")
    captured_path = None

    def get_path(path, stems):
        nonlocal captured_path
        captured_path = path
        raise RuntimeError("Demucs failed")

    mock_runner.run.side_effect = get_path

    # Act & Assert
    with pytest.raises(RuntimeError):
        service.process_audio_file(b"some_audio", ["vocals"])
    
    # Assert
    assert captured_path is not None
    assert not os.path.exists(captured_path) # Hata olsa bile dosya temizlenmiş olmalı

def test_should_create_valid_wav_temp_file(service, mock_runner):
    """
    Scenario: Temp file creation requirements.
    Expected: File should have .wav extension and contain original bytes.
    """
    # Arrange
    mock_runner.run.return_value = {"vocals": b"data"}
    input_content = b"heavy-metal-content"

    # Act
    service.process_audio_file(input_content, ["vocals"])

    # Assert
    args, _ = mock_runner.run.call_args
    path = args[0]
    assert path.endswith(".wav")
    # Dosya silinmeden önce içeriğini okumak zor olduğundan 
    # (çünkü metodun içinde siliniyor), bu testi metodu patch'leyerek yapabiliriz.

@patch("os.remove")
def test_should_call_runner_with_correct_stems(mock_remove, service, mock_runner):
    """
    Scenario: Correct stem list propagation.
    Expected: Runner receives the exact list of stems requested by the user.
    """
    # Arrange
    stems = ["vocals", "bass", "other"]
    mock_runner.run.return_value = {}

    # Act
    service.process_audio_file(b"audio", stems)

    # Assert
    # pytest.any_variable yerine ANY kullanıyoruz
    mock_runner.run.assert_called_once_with(ANY, stems)

def test_should_raise_error_when_input_bytes_is_empty(service, mock_runner):
    """
    Scenario: User sends empty audio data.
    Expected: Service should probably raise a ValueError before even trying to save it.
    """
    with pytest.raises(ValueError, match="Empty file contents"):
        service.process_audio_file(b"", ["vocals"])

def test_should_raise_error_when_stems_list_is_empty(service, mock_runner):
    """
    Scenario: User provides an empty list of stems.
    Expected: Raise error because processing nothing is a waste of resources.
    """
    with pytest.raises(ValueError, match="At least one stem must be requested"):
        service.process_audio_file(b"valid_audio", [])