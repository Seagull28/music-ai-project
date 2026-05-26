import os
import shutil
from pathlib import Path

from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


def audio_to_midi(audio_path, output_midi):
    """
    Convert audio to MIDI using Basic Pitch.
    audio_path  : path to input audio file
    output_midi : desired output .mid file path (e.g. midi/raw.mid)
    """
    output_dir = os.path.dirname(output_midi)
    os.makedirs(output_dir, exist_ok=True)

    predict_and_save(
        audio_path_list      = [audio_path],
        output_directory     = output_dir,
        model_or_model_path  = ICASSP_2022_MODEL_PATH,
        save_midi            = True,
        sonify_midi          = False,
        save_model_outputs   = False,
        save_notes           = False,
        onset_threshold      = 0.3,
        frame_threshold      = 0.2,
        minimum_note_length  = 80,
        melodia_trick        = True,
        multiple_pitch_bends = True,
    )

    # Basic Pitch names output as: {input_stem}_basic_pitch.mid
    # Find it dynamically instead of hardcoding the filename
    input_stem   = Path(audio_path).stem
    expected     = Path(output_dir) / f"{input_stem}_basic_pitch.mid"

    if expected.exists():
        shutil.move(str(expected), output_midi)
    else:
        # Fallback — find any .mid in output_dir
        mid_files = list(Path(output_dir).glob("*.mid"))
        if mid_files:
            shutil.move(str(mid_files[0]), output_midi)
        else:
            raise FileNotFoundError(
                f"Basic Pitch did not produce a MIDI file in {output_dir}\n"
                f"Expected: {expected}"
            )

    print(f"✅ MIDI saved: {output_midi}")