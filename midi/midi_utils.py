import pretty_midi


def load_midi(midi_path):

    return pretty_midi.PrettyMIDI(midi_path)


def extract_notes(midi):

    notes = []

    for instrument in midi.instruments:

        for note in instrument.notes:

            notes.append({
                "pitch": note.pitch,
                "start": note.start,
                "end": note.end,
                "velocity": note.velocity
            })

    return notes


def save_midi(midi, output_path):

    midi.write(output_path)