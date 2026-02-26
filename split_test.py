import os
import sys
import subprocess

# 1. FIX: Manually add FFmpeg DLLs to the Python search path
ffmpeg_bin = r"C:\ffmpeg\bin"
if os.path.exists(ffmpeg_bin):
    os.add_dll_directory(ffmpeg_bin)
else:
    print(f"CRITICAL: FFmpeg not found at {ffmpeg_bin}. Separation will likely fail.")

def run_separation(input_path):
    print(f"--- Starting AI Separation: {input_path} ---")
    
    # We run demucs as a module to ensure compatibility
    # --segment 7: Keeps RAM usage low
    # -d cpu: Ensures it doesn't crash your graphics card
    command = [
        sys.executable, "-m", "demucs.separate",
        "-n", "htdemucs",
        "--segment", "7",
        "-d", "cpu",
        input_path
    ]
    
    try:
        subprocess.run(command, check=True)
        print("\n✅ Success! Check the 'separated/htdemucs' folder.")
    except subprocess.CalledProcessError:
        print("\n❌ Error: The process crashed. Try a shorter audio clip.")

if __name__ == "__main__":
    target_song = "test_song.mp3"
    
    if os.path.exists(target_song):
        run_separation(target_song)
    else:
        print(f"❌ File not found: {target_song}")
        print(f"Current directory: {os.getcwd()}")
