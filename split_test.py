import subprocess
import os
import sys

def separate_audio(input_file):
    # 'htdemucs' is the high-quality model
    # We use subprocess to call the demucs CLI directly
    print(f"--- Starting AI Separation: {input_file} ---")
    
    try:
        # This command splits the song into 4 stems: vocals, drums, bass, other
        subprocess.run(["demucs", "-n", "htdemucs", input_file], check=True)
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
