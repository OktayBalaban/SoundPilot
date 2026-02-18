import pytest
import os
import subprocess
import shutil
from unittest.mock import MagicMock, patch, mock_open
from services.demucs_runner import DemucsRunner

# Configuration
RUN_HEAVY = os.getenv("RUN_HEAVY") == "true"
TEST_FILE = "tests/sample.wav"

# --- 1. SYSTEM & ENVIRONMENT SANITY CHECKS ---
# Purpose: Identify if the issue is environmental (missing binaries, paths etc.)

def test_env_ffmpeg_executability():
    """Ensure ffmpeg is not just installed but executable and responding."""
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    assert result.returncode == 0, "FFmpeg is missing or broken!"

def test_env_demucs_cli_executability():
    """Ensure demucs CLI is reachable in the current venv/path."""
    result = subprocess.run(["demucs", "--help"], capture_output=True, text=True)
    assert result.returncode == 0, "Demucs CLI is not reachable!"

def test_env_temp_dir_permissions():
    """Ensure the system allows creating and deleting temporary directories."""
    import tempfile
    test_dir = tempfile.mkdtemp()
    assert os.path.exists(test_dir)
    os.rmdir(test_dir)
    assert not os.path.exists(test_dir)

# --- 2. ISOLATED UNIT TESTS (MOCKED) ---
# Purpose: Check the internal logic of each method without running AI

@pytest.fixture
def runner():
    return DemucsRunner(model_name="htdemucs")

def test_unit_get_model_output_path_logic(runner):
    """Checks if the runner correctly predicts where Demucs will save files."""
    out_dir = "/tmp/fake_output"
    file_path = "music/my_track.mp3" # Even with extension change
    # expected: /tmp/fake_output/htdemucs/my_track
    with patch("os.path.exists", return_value=True):
        path = runner._get_model_output_path(out_dir, file_path)
        assert "htdemucs" in path
        assert "my_track" in path
        assert not path.endswith(".mp3")

def test_unit_execute_demucs_command_building(runner):
    """Verifies the subprocess command array is built correctly."""
    with patch("subprocess.run") as mocked_run:
        mocked_run.return_value = MagicMock(returncode=0)
        runner._execute_demucs("test.wav", "out/", ["vocals"])
        
        # Check call arguments
        args, _ = mocked_run.call_args
        cmd = args[0]
        assert cmd[0] == "demucs"
        assert "--two-stems" in cmd
        assert "vocals" in cmd

def test_unit_read_binary_io(runner):
    """Test the low-level binary reader."""
    m = mock_open(read_data=b"\x00\x01\x02")
    with patch("builtins.open", m):
        res = runner._read_binary("fake.wav")
        assert res == b"\x00\x01\x02"

# --- 3. COMPREHENSIVE ERROR HANDLING TESTS ---

def test_error_capture_when_demucs_crashes(runner):
    """Verify that we capture BOTH stdout and stderr when a crash occurs."""
    with patch("subprocess.run") as mocked_run:
        mocked_run.return_value = MagicMock(
            returncode=1, 
            stdout="Memory Error", 
            stderr="Critical Failure"
        )
        with pytest.raises(RuntimeError) as exc:
            runner._execute_demucs("f.wav", "o/", ["vocals"])
        
        assert "STDOUT: Memory Error" in str(exc.value)
        assert "STDERR: Critical Failure" in str(exc.value)

# --- 4. HEAVY INTEGRATION TESTS (REAL AI RUN) ---

@pytest.mark.skipif(not RUN_HEAVY, reason="Skipping heavy AI test.")
class TestDemucsHeavyIntegration:
    
    def test_heavy_full_run_workflow(self, runner):
        """Uçtan uca tüm akışı (run metodu) gerçek dosya ile test eder."""
        if not os.path.exists(TEST_FILE):
            pytest.fail(f"Integration test file missing: {TEST_FILE}")
        
        # Act
        result = runner.run(TEST_FILE, ["vocals"])
        
        # Assert
        assert isinstance(result, dict)
        assert "vocals" in result or "no_vocals" in result
        assert len(result.values()) > 0
        for data in result.values():
            assert len(data) > 0 # Byte verisi boş olmamalı

    def test_heavy_multi_stem_collection(self, runner):
        """4 kanallı (drums, bass, other, vocals) ayrıştırmayı test eder."""
        stems = ["vocals", "drums", "bass", "other"]
        result = runner.run(TEST_FILE, stems)
        
        for s in stems:
            assert s in result
            assert isinstance(result[s], bytes)