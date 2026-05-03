import pytest
import os
import subprocess
from unittest.mock import MagicMock, patch, mock_open
from services.demucs_runner import DemucsRunner

# Configuration to allow skipping heavy tests
RUN_HEAVY = os.getenv("RUN_HEAVY") == "true"
TEST_FILE = "tests/sample.wav"

@pytest.fixture
def runner():
    """
    Returns a DemucsRunner instance initialized with a test model name.
    """
    return DemucsRunner(model_name="htdemucs")

# --- UNIT TESTS (ISOLATED) ---

def test_unit_get_model_output_path_logic(runner):
    """
    Scenario: Path construction for Demucs output.
    Expected: Logic should correctly append model name and filename (without extension).
    """
    out_dir = "/tmp/fake_output"
    file_path = "music/my_track.mp3"
    
    with patch("os.path.exists", return_value=True):
        path = runner._get_model_output_path(out_dir, file_path)
        assert "htdemucs" in path
        assert "my_track" in path
        assert not path.endswith(".mp3")

def test_unit_execute_demucs_command_building(runner):
    """
    Scenario: Building the subprocess command list.
    Expected: Command list contains 'demucs', model name, and stem flags.
    """
    with patch("subprocess.run") as mocked_run:
        mocked_run.return_value = MagicMock(returncode=0)
        runner._execute_demucs("test.wav", "out/", ["vocals"])
        
        args, _ = mocked_run.call_args
        cmd = args[0]
        assert cmd[0] == "demucs"
        assert "--two-stems" in cmd
        assert "vocals" in cmd

def test_unit_read_binary_io(runner):
    """
    Scenario: Reading binary file content.
    Expected: Returns exact bytes from the mocked file.
    """
    m = mock_open(read_data=b"\x00\x01\x02")
    with patch("builtins.open", m):
        res = runner._read_binary("fake.wav")
        assert res == b"\x00\x01\x02"

def test_error_capture_when_demucs_crashes(runner):
    """
    Scenario: Demucs process fails with non-zero exit code.
    Expected: RuntimeError is raised containing both STDOUT and STDERR.
    """
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

# --- INTEGRATION TESTS (REAL EXECUTION) ---

@pytest.mark.skipif(not RUN_HEAVY, reason="Skipping heavy AI integration tests.")
class TestDemucsHeavyIntegration:
    
    def test_heavy_full_run_workflow(self, runner):
        """
        Scenario: End-to-end run with a real audio file.
        Expected: Returns a dictionary with binary data for requested stems.
        """
        if not os.path.exists(TEST_FILE):
            pytest.fail(f"Integration test file missing: {TEST_FILE}")
        
        result = runner.run(TEST_FILE, ["vocals"])
        
        assert isinstance(result, dict)
        assert "vocals" in result or "no_vocals" in result
        for data in result.values():
            assert len(data) > 0

    def test_heavy_multi_stem_collection(self, runner):
        """
        Scenario: Separation into 4 stems (drums, bass, other, vocals).
        Expected: All 4 keys exist in the result dictionary.
        """
        if not os.path.exists(TEST_FILE):
            pytest.fail(f"Integration test file missing: {TEST_FILE}")

        stems = ["vocals", "drums", "bass", "other"]
        result = runner.run(TEST_FILE, stems)
        
        for s in stems:
            assert s in result
            assert isinstance(result[s], bytes)