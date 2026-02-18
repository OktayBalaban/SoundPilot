import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app 
from api.dependencies import get_processor_service

@pytest.fixture
def client():
    """
    Returns a TestClient instance for API integration testing.
    """
    return TestClient(app)

@pytest.fixture
def mock_service():
    """
    Mocks the ProcessorService and overrides the dependency in the FastAPI app.
    Cleans up overrides after each test execution.
    """
    mock = MagicMock()
    app.dependency_overrides[get_processor_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

def test_process_audio_success_flow(client, mock_service):
    """
    Scenario: User uploads a valid audio file.
    Expected: Service layer is called, results are saved, and returns 200 JSON response.
    """
    fake_job_id = "test-uuid-123"
    fake_paths = [f"/static/{fake_job_id}/vocals.wav"]
    
    mock_service.process_audio_file.return_value = {"vocals": b"fake-data"}
    mock_service.save_results.return_value = {
        "job_id": fake_job_id,
        "paths": fake_paths
    }
    
    file_payload = {"file": ("test.wav", b"fake-audio-content", "audio/wav")}
    
    response = client.post("/api/v1/processor/process", files=file_payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["job_id"] == fake_job_id
    assert data["status"] == "completed"
    assert data["processed_files"] == fake_paths
    
    mock_service.process_audio_file.assert_called_once()
    mock_service.save_results.assert_called_once_with({"vocals": b"fake-data"})

def test_process_audio_respects_stem_selection(client, mock_service):
    """
    Scenario: User selects specific stems (e.g., only drums).
    Expected: Service receives only the requested list of stems.
    """
    mock_service.process_audio_file.return_value = {"drums": b"drums-data"}
    mock_service.save_results.return_value = {"job_id": "1", "paths": []}
    
    file_payload = {"file": ("test.wav", b"content", "audio/wav")}
    params = {"vocals": "false", "drums": "true", "bass": "false", "other": "false"}
    
    client.post("/api/v1/processor/process", files=file_payload, params=params)
    
    args, _ = mock_service.process_audio_file.call_args
    sent_stems = args[1] 
    
    assert sent_stems == ["drums"]
    assert "vocals" not in sent_stems

def test_process_audio_default_stems_when_none_selected(client, mock_service):
    """
    Scenario: No stem parameters provided in the request.
    Expected: All default stems (vocals, drums, bass, other) should be selected.
    """
    mock_service.process_audio_file.return_value = {}
    mock_service.save_results.return_value = {"job_id": "1", "paths": []}
    file_payload = {"file": ("test.wav", b"content", "audio/wav")}
    
    client.post("/api/v1/processor/process", files=file_payload)
    
    args, _ = mock_service.process_audio_file.call_args
    sent_stems = args[1]
    assert sorted(sent_stems) == sorted(["vocals", "drums", "bass", "other"])

def test_process_audio_validation_error_missing_file(client):
    """
    Scenario: Post request without the required file payload.
    Expected: 422 Unprocessable Entity returned by FastAPI.
    """
    response = client.post("/api/v1/processor/process")
    assert response.status_code == 422

def test_process_audio_internal_error_handling(client, mock_service):
    """
    Scenario: Service layer raises an unexpected exception.
    Expected: 500 Internal Server Error with a descriptive error message.
    """
    mock_service.process_audio_file.side_effect = Exception("Demucs fail")
    file_payload = {"file": ("test.wav", b"content", "audio/wav")}
    
    response = client.post("/api/v1/processor/process", files=file_payload)
    
    assert response.status_code == 500
    assert "Demucs fail" in response.json()["detail"]