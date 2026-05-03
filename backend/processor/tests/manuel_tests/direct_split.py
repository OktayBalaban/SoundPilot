import os
import sys

# Scriptin bulunduğu klasörden (manuel_tests) bir yukarı (tests) 
# ve bir daha yukarı (processor) çıkarak root'u bulalım
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..", "..")
sys.path.append(PROJECT_ROOT)

from services.demucs_runner import DemucsRunner

def run_direct_split():
    # Relative Yollar
    # BASE_DIR: tests/manuel_tests -> bir yukarı çık: tests/sample.wav
    input_file = os.path.join(BASE_DIR, "..", "sample.wav")
    output_dir = os.path.join(BASE_DIR, "outputs")

    if not os.path.exists(input_file):
        print(f"❌ Hata: {input_file} yerinde yok!")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"🚀 İşlem başladı: {input_file}")
    runner = DemucsRunner()

    try:
        # Doğrudan motoru çalıştır (4 stem)
        stems_dict = runner.run(input_file, ["vocals", "drums", "bass", "other"])

        for name, data in stems_dict.items():
            out_path = os.path.join(output_dir, f"{name}.wav")
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"✅ Kaydedildi: {name}.wav")

        print(f"\n🎉 Bitti! Çıktılar şurada: {output_dir}")

    except Exception as e:
        print(f"🔥 Motor Hatası: {e}")

if __name__ == "__main__":
    run_direct_split()