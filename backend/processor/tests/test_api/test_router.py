import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from main import app 
from api.dependencies import get_processor_service

@pytest.fixture
def client():
    """
    Provides a TestClient that doesn't raise exceptions, 
    allowing the global exception handler to do its job.
    """
    # raise_server_exceptions=False: Bu kritik ayar hatanın 
    # yukarı fırlamasını engeller ve JSONResponse dönmesini sağlar.
    return TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def mock_service():
    """
    Standard fixture to mock the ProcessorService.
    Ensures dependency overrides are cleared after each test.
    """
    mock = MagicMock()
    app.dependency_overrides[get_processor_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

def test_should_return_success_status_when_valid_file_is_provided(client, mock_service):
    """
    Scenario: User uploads a valid audio file.
    Expected: 200 OK status.
    """
    # Arrange
    mock_service.process_audio_file.return_value = b"fake-processed-audio"
    file_payload = {"file": ("test.wav", b"fake-audio", "audio/wav")}
    
    # Act
    response = client.post("/process", files=file_payload)
    
    # Assert
    assert response.status_code == 200

def test_should_return_validation_error_when_file_is_missing(client):
    """
    Scenario: Missing file upload.
    Expected: 422 Unprocessable Entity.
    """
    # Act
    response = client.post("/process")
    
    # Assert
    assert response.status_code == 422

def test_should_delegate_to_service_and_return_processed_audio_stream(client, mock_service):
    """
    Scenario: Successful delegation to service layer.
    Expected: Audio stream returned with correct headers and content.
    """
    # Arrange
    fake_content = b"processed-audio-bytes"
    mock_service.process_audio_file.return_value = fake_content
    file_payload = {"file": ("test.wav", b"input", "audio/wav")}
    
    # Act
    response = client.post("/process", files=file_payload)
    
    # Assert
    assert response.status_code == 200
    assert response.content == fake_content
    assert response.headers["content-type"] == "audio/wav"
    assert "processed_test.wav" in response.headers["content-disposition"]

def test_should_return_500_with_meaningful_message_when_service_fails(client, mock_service):
    """
    Scenario: ProcessorService raises an exception (e.g., Demucs failure).
    Expected: API should return 500 status code with a clean error message from the global handler.
    """
    # Arrange
    mock_service.process_audio_file.side_effect = Exception("Demucs binary not found")
    file_payload = {"file": ("test.wav", b"fake-audio", "audio/wav")}
    
    # Act
    response = client.post("/process", files=file_payload)
    
    # Assert
    assert response.status_code == 500
    assert response.json()["detail"] == "Audio processing failed: Demucs binary not found"