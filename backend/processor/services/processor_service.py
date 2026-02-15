import tempfile
import os
from typing import List, Dict

class ProcessorService:
    def __init__(self, runner):
        self.runner = runner

    def process_audio_file(self, file_contents: bytes, stems: List[str]) -> Dict[str, bytes]:
        """
        Coordinates the audio processing workflow:
        Input Bytes -> Temp File -> AI Runner -> Multi-Stem Dictionary
        """
        if not file_contents:
            raise ValueError("Empty file contents")
        if not stems:
            raise ValueError("At least one stem must be requested")
        # Sorumluluk 1: Geçici dosyayı oluştur
        temp_input_path = self._create_temp_file(file_contents)
        
        try:
            # Sorumluluk 2: Runner'ı tetikle ve sonucu al
            return self.runner.run(temp_input_path, stems)
        finally:
            # Sorumluluk 3: Temizlik yap (Input dosyasını sil)
            self._safe_remove(temp_input_path)

    def _create_temp_file(self, contents: bytes) -> str:
        # delete=False önemli çünkü Runner bu dosyayı kendi sürecinde okuyacak
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(contents)
            return temp_file.name

    def _safe_remove(self, path: str):
        if os.path.exists(path):
            os.remove(path)