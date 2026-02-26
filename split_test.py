import os
import sys
import subprocess

# 1. SETUP DLLs for FFmpeg
ffmpeg_bin = r"C:\ffmpeg\bin"
if os.path.exists(ffmpeg_bin):
    os.add_dll_directory(ffmpeg_bin)

def clear_system_ram():
    """Triggers RAMMap64 to flush System Standby List (Cached RAM)"""
    print("--- Cleaning System RAM Cache ---")
    try:
        # Runs the command we just moved to System32
        # -EmptyStandbyList is the specific flag for RAMMap
        subprocess.run(["RAMMap64.exe", "-EmptyStandbyList"], check=True)
        print("✅ Standby RAM Cleared.")
    except FileNotFoundError:
        print("⚠️ Warning: RAMMap64.exe not found in System32. Skipping RAM clear.")
    except Exception as e:
        print(f"⚠️ Could not clear RAM: {e}")

def run_6stem_separation(input_path):
    # Clear RAM before starting the heavy 6-stem model
    clear_system_ram()
    
    print(f"--- Starting 6-Stem AI Separation: {input_path} ---")
    
    command = [
        sys.executable, "-m", "demucs.separate",
        "-n", "htdemucs_6s",
        "--segment", "7",
        "-d", "cpu",
        input_path
    ]
    
    try:
        subprocess.run(command, check=True)
        print("\n✅ Success! Check 'separated/htdemucs_6s'.")
    except subprocess.CalledProcessError:
        print("\n❌ Error: The process crashed. Check your system resources.")

if __name__ == "__main__":
    target_song = "test_song.mp3"
    if os.path.exists(target_song):
        run_6stem_separation(target_song)
    else:
        print(f"❌ File not found: {target_song}")
