import os
import argparse

from core.gpu_utils import get_device
from core.audio_cleaner import clean_audio
from core.stem_separator import separate_stems
from core.lyrics_engine import LyricsEngine
from core.subtitle_exporter import export_srt
# INJECT NEW TIMING MODULES HERE:
from core.timing_engine import generate_tempo_grid

from exports.pdf_exporter import export_lyrics_pdf

from midi.advanced_midi import audio_to_midi
from midi.instrument_arranger import arrange_for_instrument
# SWAP TO THE TIMELINE EXTRACTOR:
from midi.note_extractor import extract_midi_notes_with_timeline
from midi.midi_post_processor import MidiPostProcessor

from sheets.musicxml_exporter import midi_to_musicxml
from sheets.html_sheet_generator import generate_html_sheet


def ensure_dirs(base_output):
    dirs = ["cleaned", "lyrics", "stems", "midi", "sheets"]
    for d in dirs:
        os.makedirs(os.path.join(base_output, d), exist_ok=True)


def process_song(input_audio, language="en", whisper_model="small", instrument="piano"):
    raw_device = get_device()
    device = "cuda" if "cuda" in str(raw_device).lower() else "cpu"

    song_name = os.path.splitext(os.path.basename(input_audio))[0]
    base_output = os.path.join("output", song_name)
    ensure_dirs(base_output)

    print("\n════════════════════════════════════════════════════════════")
    print("  🎵 MUSIC AI PIPELINE (TIMELINE GRID ACTIVE)")
    print("════════════════════════════════════════════════════════════")
    print(f"\nDevice         : {device}")
    print(f"Language       : {language}")
    print(f"Whisper Model  : {whisper_model}")
    print(f"Instrument     : {instrument}")

    # =====================================================
    # STEP 1 — AUDIO CLEANING
    # =====================================================
    print("\nSTEP 1 — Audio Cleaning")
    cleaned_audio = os.path.join(base_output, "cleaned", "cleaned.wav")
    clean_audio(input_audio, cleaned_audio)
    print("✅ Cleaned audio generated")

    # =====================================================
    # EXTRACTION PREPARATION — CENTRALIZED TIMING DETECTION
    # =====================================================
    print("\nINTERMEDIATE STEP — Constructing Unified Music Timeline Grid")
    tempo_grid = generate_tempo_grid(cleaned_audio, beats_per_bar=4)
    print(f"✅ Extracted Structural Tempo: {tempo_grid['global_bpm']} BPM")
    print(f"✅ Mapped Time Signature     : {tempo_grid['time_signature']}")

    # =====================================================
    # STEP 2 — STEM SEPARATION
    # =====================================================
    print("\nSTEP 2 — Stem Separation")
    stems = separate_stems(cleaned_audio, os.path.join(base_output, "stems"))
    vocals_path = stems["vocals"]
    instrumental_path = stems["instrumental"]
    print("✅ Vocals extracted\n✅ Instrumental extracted")

    # =====================================================
    # STEP 3 — LYRICS TRANSCRIPTION
    # =====================================================
    print("\nSTEP 3 — Lyrics Transcription")
    lyrics_engine = LyricsEngine(device=device, model_size=whisper_model)
    transcription = lyrics_engine.transcribe_audio(vocals_path, language=language)

    if isinstance(transcription, dict):
        segments = transcription.get("segments", [])
        full_text = transcription.get("text", "")
    else:
        segments = transcription
        full_text = ""

    lyrics_dir = os.path.join(base_output, "lyrics")
    lyrics_txt = os.path.join(lyrics_dir, "lyrics.txt")
    lyrics_srt = os.path.join(lyrics_dir, "lyrics.srt")
    lyrics_pdf = os.path.join(lyrics_dir, "lyrics.pdf")

    with open(lyrics_txt, "w", encoding="utf-8") as f:
        if full_text.strip():
            f.write(full_text)
        else:
            for seg in segments:
                line = seg.text.strip() if hasattr(seg, "text") else str(seg).strip()
                f.write(line + "\n")

    if isinstance(segments, list) and len(segments) > 0:
        first_seg = segments[0]
        if hasattr(first_seg, "start") or (isinstance(first_seg, dict) and "start" in first_seg):
            export_srt(segments, lyrics_srt)

    export_lyrics_pdf(lyrics_txt, lyrics_pdf)
    print("✅ Lyrics generated")

    
    # =====================================================
    # STEP 4 — MIDI GENERATION & TIMELINE EXTRACTION
    # =====================================================

    print("\nSTEP 4 — MIDI Generation & Timeline Extraction")

    midi_dir = os.path.join(base_output, "midi")

    # ---------------------------------
    # RAW MIDI FROM AUDIO
    # ---------------------------------

    raw_midi = os.path.join(
        midi_dir,
        "raw.mid"
    )

    audio_to_midi(
        instrumental_path,
        raw_midi
    )

    # ---------------------------------
    # CLEAN / QUANTIZED MIDI
    # ---------------------------------

    processed_midi = os.path.join(
        midi_dir,
        "processed.mid"
    )

    processor = MidiPostProcessor()

    processor.process(
        raw_midi,
        processed_midi
    )

    # ---------------------------------
    # INSTRUMENT ARRANGEMENT
    # ---------------------------------

    arranged_midi = os.path.join(
        midi_dir,
        f"{instrument}_arrangement.mid"
    )

    arrange_for_instrument(
        processed_midi,
        arranged_midi,
        instrument
    )

    print("✅ MIDI generated")

    # ---------------------------------
    # NOTE TIMELINE EXTRACTION
    # ---------------------------------

    notes_json = os.path.join(
        midi_dir,
        f"{instrument}_notes.json"
    )

    extract_midi_notes_with_timeline(
        arranged_midi,
        tempo_grid,
        notes_json
    )

    # =====================================================
    # STEP 5 — MUSICXML EXPORT
    # =====================================================
    print("\nSTEP 5 — MusicXML Export")
    sheets_dir = os.path.join(base_output, "sheets")
    musicxml_path = os.path.join(sheets_dir, f"{instrument}.musicxml")
    
    midi_to_musicxml(arranged_midi, musicxml_path)
    print("✅ MusicXML exported")

    # =====================================================
    # STEP 6 — HTML INTERACTIVE SHEET LOOKUP
    # =====================================================
    print("\nSTEP 6 — HTML Sheet")
    html_sheet = os.path.join(sheets_dir, f"{instrument}_sheet.html")

    generate_html_sheet(
        musicxml_path,
        html_sheet,
        song_name,
        instrument,
        instrumental_path,
        arranged_midi,
        notes_json # 👈 Pass this to let the parser pull real timestamp seconds
    )
    print("✅ HTML sheet generated")

    print("\n════════════════════════════════════════════════════════════")
    print("  ✅ PIPELINE COMPLETE (TIMELINE CONVERGED)")
    print("════════════════════════════════════════════════════════════")
    print(f"\n📂 Output Folder: {base_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("--language", default="en")
    parser.add_argument("--whisper-model", default="small")
    parser.add_argument("--instrument", default="piano")
    args = parser.parse_args()

    process_song(args.audio, args.language, args.whisper_model, args.instrument)