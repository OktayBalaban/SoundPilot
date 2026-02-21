import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

# FastAPI'nin sağladığı test istemcisi
client = TestClient(app)

@patch("api.router.storage_service.save_result")
def test_upload_file_endpoint_returns_success(mock_save_result):
    """
    Scenario: Uploading a file to the storage service via HTTP POST.
    Expected: HTTP 200 and a JSON response containing the file URL.
    """
    # Mock the return value of the storage service
    expected_url = "http://localhost:8001/files/test-job/vocals.wav"
    mock_save_result.return_value = expected_url

    # Create dummy file data
    file_data = {"file": ("vocals.wav", b"fake-audio-bytes", "audio/wav")}

    response = client.post(
        "/upload/test-job?stem_name=vocals",
        files=file_data
    )

    assert response.status_code == 200
    assert response.json() == {"url": expected_url}
    mock_save_result.assert_called_once_with("test-job", "vocals", b"fake-audio-bytes")

@patch("api.router.storage_service.delete_job")
def test_delete_job_endpoint_returns_success(mock_delete_job):
    """
    Scenario: Deleting a job's files via HTTP DELETE.
    Expected: HTTP 200 and a success status message.
    """
    response = client.delete("/jobs/test-job")

    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}
    mock_delete_job.assert_called_once_with("test-job")