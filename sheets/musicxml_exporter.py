from music21 import converter


def midi_to_musicxml(
    midi_path,
    output_xml
):

    score = converter.parse(midi_path)

    score.write(
        "musicxml",
        fp=output_xml
    )