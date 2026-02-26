"""
import os
os.add_dll_directory(r"C:\ffmpeg\bin")
import subprocess
import sys

def separate_audio(input_file):
    #Separates audio using memory-optimized settings for Demucs.
    
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

ffmpeg_bin = r"C:\ffmpeg\bin"
if os.path.exists(ffmpeg_bin):
    os.add_dll_directory(ffmpeg_bin)

os.environ["TORCHAUDIO_USE_BACKEND"] = "soundfile"

try:
    import torch
    import demucs.api
    import soundfile
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Executable: {sys.executable}")
    sys.exit(1)

def run_separation(input_path):
    print(f"Processing: {input_path}")
    
    separator = demucs.api.Separator(
        model="htdemucs",
        device="cpu", 
        segment=7,
        overlap=0.1
    )

    try:
        origin, separated = separator.separate_audio_file(input_path)
        
        base_name = os.path.splitext(input_path)[0]
        out_dir = os.path.join("separated", "htdemucs", base_name)
        os.makedirs(out_dir, exist_ok=True)

        for name, tensor in separated.items():
            stem_path = os.path.join(out_dir, f"{name}.wav")
            demucs.api.save_audio(tensor, stem_path, samplerate=separator.samplerate)
            print(f"Saved: {stem_path}")

        print("Done.")

    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    file_to_process = "test_song.mp3"
    if os.path.exists(file_to_process):
        run_separation(file_to_process)
    else:
        print(f"File not found: {file_to_process}")

