import os
import sys
import subprocess

# Ensure FFmpeg is found for saving audio
ffmpeg_bin = r"C:\ffmpeg\bin"
if os.path.exists(ffmpeg_bin):
    os.add_dll_directory(ffmpeg_bin)

def run_bulletproof_separation(input_path):
    print("--- MODE: BULLETPROOF (Lowest RAM Usage) ---")
    print(f"--- Processing: {input_path} ---")
    
    # -n htdemucs_6s: The 6-stem model (Vocals, Drums, Bass, Piano, Guitar, Other)
    # --segment 2: Smallest window for RAM safety
    # --shifts 1: No extra passes (Fastest speed)
    # --overlap 0.1: Minimal blending memory
    # -j 1: Single CPU core to prevent system freeze
    command = [
        sys.executable, "-m", "demucs.separate",
        "-n", "htdemucs_6s",
        "--segment", "2",
        "--shifts", "1",
        "--overlap", "0.1",
        "-j", "1",
        "-d", "cpu",
        input_path
    ]
    
    try:
        # We run the command and let it output directly to your CMD for the progress bar
        subprocess.run(command, check=True)
        print("\n✅ Bulletproof Separation Finished!")
        print(f"Check folder: separated/htdemucs_6s/{os.path.splitext(input_path)[0]}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: AI Process failed (Exit Code {e.returncode}).")
        print("Tip: Close all other apps and ensure you have 2GB+ free RAM.")

if __name__ == "__main__":
    target = "test_song.mp3"
    
    if os.path.exists(target):
        run_bulletproof_separation(target)
    else:
        print(f"❌ File not found: {target}")