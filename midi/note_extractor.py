import json
import pretty_midi


def extract_midi_notes_with_timeline(
    midi_path,
    tempo_grid,
    output_json
):
    """
    Extract note timings from MIDI using pretty_midi.
    pretty_midi converts everything to real seconds automatically —
    no manual BPM math needed, so timestamps always match audio playback.
    """

    pm  = pretty_midi.PrettyMIDI(midi_path)
    bpm = tempo_grid.get("global_bpm", 120)

    # Safety clamp
    if bpm > 180:
        bpm = bpm / 2

    notes_data = []

    for instrument in pm.instruments:
        for note in instrument.notes:

            # pretty_midi gives start/end in real seconds — exactly what
            # the browser's audioTrack.currentTime reports
            notes_data.append({
                "pitch":    int(note.pitch),
                "start":    round(float(note.start), 3),
                "end":      round(float(note.end),   3),
                "velocity": int(note.velocity),
            })

    # Sort by start time
    notes_data.sort(key=lambda x: x["start"])

    # Sanity check — warn if notes seem too short (common BPM mismatch symptom)
    if notes_data:
        avg_dur = sum(n["end"] - n["start"] for n in notes_data) / len(notes_data)
        if avg_dur < 0.05:
            print(f"  ⚠️  Average note duration is {avg_dur:.3f}s — notes may be too short to see")
        else:
            print(f"  ✅ Avg note duration: {avg_dur:.3f}s  |  Range: "
                  f"{notes_data[0]['start']:.2f}s – {notes_data[-1]['end']:.2f}s")

    final_data = {
        "bpm":   bpm,
        "notes": notes_data,
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)

    print(f"  ✅ Extracted {len(notes_data)} notes → {output_json}")