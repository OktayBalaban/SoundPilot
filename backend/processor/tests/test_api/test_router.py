import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app 
from api.dependencies import get_processor_service

@pytest.fixture
def client():
    """
    Global exception handler'ı test edebilmek için raise_server_exceptions=False.
    """
    return TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def mock_service():
    """
    ProcessorService'i mock'lar ve her testten sonra override'ı temizler.
    """
    mock = MagicMock()
    app.dependency_overrides[get_processor_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

def test_process_audio_success_flow(client, mock_service):
    """
    Senaryo: Kullanıcı geçerli bir dosya yükler.
    Beklenen: Servis katmanı çağrılmalı, dosyalar kaydedilmeli ve 200 JSON dönmeli.
    """
    # Arrange
    fake_job_id = "test-uuid-123"
    fake_paths = [f"/static/{fake_job_id}/vocals.wav"]
    
    # Mock zinciri: Önce bytes döner, sonra kaydedilen dosya bilgilerini döner.
    mock_service.process_audio_file.return_value = {"vocals": b"fake-data"}
    mock_service.save_results.return_value = {
        "job_id": fake_job_id,
        "paths": fake_paths
    }
    
    file_payload = {"file": ("test.wav", b"fake-audio-content", "audio/wav")}
    
    # Act
    response = client.post("/api/v1/processor/process", files=file_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Yanıt içeriği doğrulaması
    assert data["job_id"] == fake_job_id
    assert data["status"] == "completed"
    assert data["processed_files"] == fake_paths
    
    # Servis etkileşimi doğrulaması
    mock_service.process_audio_file.assert_called_once()
    mock_service.save_results.assert_called_once_with({"vocals": b"fake-data"})

def test_process_audio_respects_stem_selection(client, mock_service):
    """
    Senaryo: Kullanıcı sadece belirli enstrümanları seçer (örneğin sadece drums).
    Beklenen: Servise sadece seçilen stem listesi iletilmeli.
    """
    # Arrange
    mock_service.process_audio_file.return_value = {"drums": b"drums-data"}
    mock_service.save_results.return_value = {"job_id": "1", "paths": []}
    
    file_payload = {"file": ("test.wav", b"content", "audio/wav")}
    # Sadece drums=true, diğerleri false
    params = {"vocals": "false", "drums": "true", "bass": "false", "other": "false"}
    
    # Act
    client.post("/api/v1/processor/process", files=file_payload, params=params)
    
    # Assert
    # call_args[0] positional argument'ları verir. stems listesi 2. argümandı.
    args, _ = mock_service.process_audio_file.call_args
    sent_stems = args[1] 
    
    assert sent_stems == ["drums"]
    assert "vocals" not in sent_stems

def test_process_audio_default_stems_when_none_selected(client, mock_service):
    """
    Senaryo: Seçim parametreleri gönderilmezse.
    Beklenen: Varsayılan olarak tüm stem'ler (vocals, drums, bass, other) seçilmeli.
    """
    # Arrange
    mock_service.process_audio_file.return_value = {}
    mock_service.save_results.return_value = {"job_id": "1", "paths": []}
    file_payload = {"file": ("test.wav", b"content", "audio/wav")}
    
    # Act
    client.post("/api/v1/processor/process", files=file_payload)
    
    # Assert
    args, _ = mock_service.process_audio_file.call_args
    sent_stems = args[1]
    assert sorted(sent_stems) == sorted(["vocals", "drums", "bass", "other"])

def test_process_audio_validation_error_missing_file(client):
    """
    Senaryo: Hiç dosya gönderilmezse.
    Beklenen: 422 Unprocessable Entity.
    """
    response = client.post("/api/v1/processor/process")
    assert response.status_code == 422

def test_process_audio_internal_error_handling(client, mock_service):
    """
    Senaryo: Servis katmanı beklenmedik bir hata fırlatırsa.
    Beklenen: 500 hatası ve temiz bir hata mesajı.
    """
    # Arrange
    mock_service.process_audio_file.side_effect = Exception("Demucs fail")
    file_payload = {"file": ("test.wav", b"content", "audio/wav")}
    
    # Act
    response = client.post("/api/v1/processor/process", files=file_payload)
    
    # Assert
    assert response.status_code == 500
    # Global exception handler'dan dönen formatı kontrol et
    assert "Demucs fail" in response.json()["detail"]