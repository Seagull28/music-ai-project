import shutil


def arrange_for_instrument(
    midi_path,
    output_path,
    instrument="piano"
):

    shutil.copy(midi_path, output_path)