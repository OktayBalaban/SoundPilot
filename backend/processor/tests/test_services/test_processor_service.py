import pytest
import os
from unittest.mock import MagicMock, ANY
from services.processor_service import ProcessorService

@pytest.fixture
def mock_runner():
    return MagicMock()

@pytest.fixture
def mock_storage():
    storage = MagicMock()
    storage.save_result.return_value = "http://fake-url.com/audio.wav"
    return storage

@pytest.fixture
def service(mock_runner, mock_storage):
    return ProcessorService(mock_runner, mock_storage)

def test_should_return_dict_when_processing_is_successful(service, mock_runner):
    """
    Scenario: Normal operational flow.
    Expected: Service returns the dictionary provided by the runner.
    """
    expected_output = {"vocals": b"vocal_data", "drums": b"drum_data"}
    mock_runner.run.return_value = expected_output
    
    result = service.process_audio_file(b"fake_audio", ["vocals", "drums"])
    
    assert result == expected_output
    mock_runner.run.assert_called_once()

def test_should_ensure_temp_file_is_deleted_after_processing(service, mock_runner):
    """
    Scenario: Ensure no temporary files are leaked on the disk.
    Expected: The temp file created must not exist after function execution.
    """
    mock_runner.run.return_value = {"vocals": b"data"}
    captured_path = None

    def mock_run(path, stems):
        nonlocal captured_path
        captured_path = path
        assert os.path.exists(path)
        return {"vocals": b"data"}

    mock_runner.run.side_effect = mock_run
    service.process_audio_file(b"content", ["vocals"])

    assert captured_path is not None
    assert not os.path.exists(captured_path)

def test_should_cleanup_temp_file_even_if_runner_raises_exception(service, mock_runner):
    """
    Scenario: Runner crashes during execution.
    Expected: Service must still delete the input temp file.
    """
    captured_path = None

    def get_path(path, stems):
        nonlocal captured_path
        captured_path = path
        raise RuntimeError("Demucs failed")

    mock_runner.run.side_effect = get_path

    with pytest.raises(RuntimeError):
        service.process_audio_file(b"some_audio", ["vocals"])
    
    assert captured_path is not None
    assert not os.path.exists(captured_path)

def test_should_raise_error_when_input_bytes_is_empty(service):
    """
    Scenario: User sends empty audio data.
    Expected: Raise ValueError.
    """
    with pytest.raises(ValueError, match="Empty file contents"):
        service.process_audio_file(b"", ["vocals"])

def test_save_results_delegates_to_storage_service(service, mock_storage):
    """
    Scenario: Saving processed data.
    Expected: Storage service should be called for each stem and return a job info.
    """
    processed_data = {
        "vocals": b"vocal-bytes",
        "drums": b"drum-bytes"
    }

    result = service.save_results(processed_data)

    assert "job_id" in result
    assert len(result["paths"]) == 2
    assert mock_storage.save_result.call_count == 2
    mock_storage.save_result.assert_any_call(ANY, "vocals", b"vocal-bytes")
    mock_storage.save_result.assert_any_call(ANY, "drums", b"drum-bytes")

def test_cleanup_job_removes_data_via_storage(service, mock_storage):
    """
    Scenario: Job cleanup is requested.
    Expected: StorageService.delete_job is called.
    """
    service.cleanup_job("test-job-id")
    mock_storage.delete_job.assert_called_once_with("test-job-id")