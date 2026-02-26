"""import subprocess
import os
import sys

def separate_audio(input_file):
    # 'htdemucs' is the high-quality model
    # We use subprocess to call the demucs CLI directly
    print(f"--- Starting AI Separation: {input_file} ---")
    
    try:
        # This command splits the song into 4 stems: vocals, drums, bass, other
        subprocess.run(["demucs", "-n", "htdemucs_ft","--segment","12", input_file], check=True)
        print("\n✅ Success! Check the 'separated' folder for your tracks.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during separation: {e}")
    except FileNotFoundError:
        print("\n❌ Error: Demucs or FFmpeg not found in PATH.")

if __name__ == "__main__":
    # Put a song named 'test_song.mp3' in your project folder
    target_song = "test_song.mp3"
    
    if os.path.exists(target_song):
        separate_audio(target_song)
    else:
        print(f"❌ File not found: {target_song}")
        print("Please place an mp3 file named 'test_song.mp3' in this folder.")
"""
import os
os.add_dll_directory(r"C:\ffmpeg\bin")
import subprocess
import sys

def separate_audio(input_file):
    """
    Separates audio using memory-optimized settings for Demucs.
    """
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
