"""
import os
os.add_dll_directory(r"C:\ffmpeg\bin")
import subprocess
import sys

def separate_audio(input_file):
    Separates audio using memory-optimized settings for Demucs.
    
    print(f"--- Starting Optimized AI Separation: {input_file} ---")
    
    # Flags explained:
    # "-n htdemucs": The high-quality hybrid transformer model.
    # "--segment 7": CRITICAL. Processes in 7-second chunks to save RAM. 
    #                HTDemucs models support max ~7.8s chunks.
    # "--overlap 0.1": Reduces memory used for blending chunks.
    # "-j 1": Limits to 1 parallel job. Multiple jobs multiply RAM usage.
    
    command = [
        "demucs", 
        "-n", "htdemucs", 
        "--segment", "7", 
        "--overlap", "0.1",
        "-j", "1",
        "--float32",
        input_file
    ]
    
    try:
        # Run the command and pipe output to the console so you see progress
        subprocess.run(command, check=True)
        print("\n✅ Success! Check the 'separated/htdemucs' folder.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: The process crashed. This is likely still a memory issue.")
        print("Try closing other apps (Chrome, etc.) or using a shorter audio clip.")
    except FileNotFoundError:
        print("\n❌ Error: Demucs not found. Run 'pip install demucs' first.")

if __name__ == "__main__":
    target_song = "test_song.mp3"
    
    if os.path.exists(target_song):
        separate_audio(target_song)
    else:
        print(f"❌ File not found: {target_song}")
        print(f"Current directory: {os.getcwd()}")
"""
import os
import sys

# 1. FIX: Manually add FFmpeg DLLs to the Python search path (Required for Windows)
# Ensure this path matches where you extracted the "full-shared" FFmpeg
ffmpeg_bin = r"C:\ffmpeg\bin"
if os.path.exists(ffmpeg_bin):
    os.add_dll_directory(ffmpeg_bin)
else:
    print(f"CRITICAL: FFmpeg not found at {ffmpeg_bin}. Please install full-shared version.")

# 2. FIX: Bypass libtorchcodec/torchaudio issues by using the 'soundfile' backend
# This avoids the "Could not load libtorchcodec" error entirely.
os.environ["TORCHAUDIO_USE_BACKEND"] = "soundfile"

try:
    import demucs.api
    import torch
except ImportError:
    print("Error: Demucs or Torch not found. Run: pip install demucs soundfile")
    sys.exit(1)

def run_optimized_separation(input_path):
    """
    Uses the Demucs API for direct control over memory and audio processing.
    """
    print(f"--- Starting Separation: {input_path} ---")
    
    # Initialize the separator with memory-optimized parameters
    # 'htdemucs' is the high-quality model.
    # 'segment=7': Process in small chunks to save RAM (Max for HTDemucs is ~7.8s).
    # 'device="cpu"': Recommended if your GPU has less than 8GB VRAM.
    separator = demucs.api.Separator(
        model="htdemucs",
        device="cpu", 
        segment=7,
        overlap=0.1
    )

    try:
        # Separate the file
        # The API handles loading and splitting internally
        origin, separated = separator.separate_audio_file(input_path)
        
        # Create output directory
        out_dir = os.path.join("separated", "htdemucs", os.path.splitext(input_path)[0])
        os.makedirs(out_dir, exist_ok=True)

        # Save each stem (vocals, drums, bass, other)
        for name, tensor in separated.items():
            stem_path = os.path.join(out_dir, f"{name}.wav")
            demucs.api.save_audio(tensor, stem_path, samplerate=separator.samplerate)
            print(f"Saved: {stem_path}")

        print("\n✅ Separation Complete!")

    except Exception as e:
        print(f"\n❌ Process failed: {e}")
        print("Tip: If this is a memory crash, try an even smaller 'segment' (e.g., 4).")

if __name__ == "__main__":
    SONG_NAME = "test_song.mp3"
    
    if os.path.exists(SONG_NAME):
        run_optimized_separation(SONG_NAME)
    else:
        print(f"❌ File not found: {SONG_NAME}")
