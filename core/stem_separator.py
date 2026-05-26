import subprocess
import os
import sys


def separate_stems(
    audio_path,
    output_dir
):

    cmd = [
        sys.executable,
        "-m",
        "demucs",

        "--two-stems",
        "vocals",

        "-o",
        output_dir,

        audio_path
    ]

    subprocess.run(
        cmd,
        check=True
    )

    # -----------------------------------
    # OUTPUT FOLDER
    # -----------------------------------

    input_name = os.path.splitext(
        os.path.basename(audio_path)
    )[0]

    demucs_folder = os.path.join(
        output_dir,
        "htdemucs",
        input_name
    )

    vocals = os.path.join(
        demucs_folder,
        "vocals.wav"
    )

    instrumental = os.path.join(
        demucs_folder,
        "no_vocals.wav"
    )

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not os.path.exists(vocals):

        raise FileNotFoundError(
            f"Vocals stem missing: {vocals}"
        )

    if not os.path.exists(instrumental):

        raise FileNotFoundError(
            f"Instrumental stem missing: {instrumental}"
        )

    return {
        "vocals": vocals,
        "instrumental": instrumental
    }