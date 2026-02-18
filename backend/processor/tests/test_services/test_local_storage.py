import pytest
import os
import shutil
from services.local_storage import LocalStorageService

@pytest.fixture
def storage_setup(tmp_path):
    """
    Sets up a temporary directory for local storage testing.
    """
    base_path = tmp_path / "outputs"
    static_prefix = "/static"
    service = LocalStorageService(str(base_path), static_prefix)
    return service, base_path

def test_should_save_file_and_return_correct_url(storage_setup):
    """
    Scenario: Saving a processed audio stem to local storage.
    Expected: File exists on disk and returned URL follows the defined pattern.
    """
    service, base_path = storage_setup
    job_id = "test-job-1"
    stem_name = "vocals"
    data = b"fake-audio-content"

    url = service.save_result(job_id, stem_name, data)

    expected_path = base_path / job_id / "vocals.wav"
    assert url == "/static/test-job-1/vocals.wav"
    assert expected_path.exists()
    assert expected_path.read_bytes() == data

def test_should_remove_all_job_files_on_cleanup(storage_setup):
    """
    Scenario: Deleting a job directory after processing or manual cleanup.
    Expected: The entire job folder is removed from the filesystem.
    """
    service, base_path = storage_setup
    job_id = "cleanup-job"
    service.save_result(job_id, "drums", b"data")
    
    assert (base_path / job_id).exists()
    
    service.delete_job(job_id)
    assert not (base_path / job_id).exists()