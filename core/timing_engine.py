# core/timing_engine.py

import librosa
import numpy as np

def generate_tempo_grid(audio_path, beats_per_bar=4):
    """
    Analyzes the audio file to calculate a global BPM, pinpoint precise beat positions,
    and construct a master lookup grid that maps seconds to musical measures and beats.
    """
    # Load audio explicitly at default mono/sample rate for consistent analysis
    y, sr = librosa.load(audio_path, sr=None, mono=True)
    
    # Extract tempo and individual beat timestamps
    tempo_array, beat_times = librosa.beat.beat_track(y=y, sr=sr)
    global_bpm = float(tempo_array[0]) if isinstance(tempo_array, np.ndarray) else float(tempo_array)
    
    measures = []
    measure_count = 1
    
    # Chunk flat beat detections into measures based on the time signature numerator
    for i in range(0, len(beat_times), beats_per_bar):
        bar_beats = beat_times[i : i + beats_per_bar]
        if len(bar_beats) > 0:
            # Estimate where this measure ends based on the duration of its internal beats
            if len(bar_beats) > 1:
                avg_beat_gap = float(bar_beats[-1] - bar_beats[-2])
                end_time = float(bar_beats[-1] + avg_beat_gap)
            else:
                end_time = float(bar_beats[0] + 0.5)
                
            measures.append({
                "measure": measure_count,
                "start_time": float(bar_beats[0]),
                "end_time": end_time,
                "beat_timestamps": [float(b) for b in bar_beats]
            })
            measure_count += 1
            
    return {
        "global_bpm": round(global_bpm, 2),
        "time_signature": f"{beats_per_bar}/4",
        "measures": measures
    }

def quantize_notes_to_grid(raw_notes, tempo_grid):
    """
    Translates raw absolute-second note events into a unified, quantized musical map.
    """
    quantized_notes = []
    measures = tempo_grid["measures"]
    
    for note in raw_notes:
        start_sec = note["start"]
        end_sec = note["end"]
        
        # Locate the measure this note lands in
        target_measure = None
        for m in measures:
            if m["start_time"] <= start_sec <= m["end_time"]:
                target_measure = m
                break
        
        if not target_measure:
            # Fallback to nearest boundary if edge anomalies happen
            target_measure = measures[0] if start_sec < measures[0]["start_time"] else measures[-1]
            
        # Match to closest beat timestamp inside that measure
        beat_times = target_measure["beat_timestamps"]
        closest_beat_idx = min(range(len(beat_times)), key=lambda i: abs(beat_times[i] - start_sec))
        
        # Musical beats are 1-indexed (Beat 1, Beat 2, Beat 3, Beat 4)
        musical_beat = closest_beat_idx + 1
        
        # Quantize the duration to the nearest 16th-note subdivision
        avg_beat_len = (target_measure["end_time"] - target_measure["start_time"]) / len(beat_times)
        raw_duration_beats = (end_sec - start_sec) / avg_beat_len
        quantized_duration = round(raw_duration_beats * 4) / 4  # Snaps to 0.25 steps
        
        quantized_notes.append({
            "pitch": int(note["pitch"]),
            "start_time_secs": float(start_sec),
            "end_time_secs": float(end_sec),
            "velocity": int(note.get("velocity", 64)),
            "measure": int(target_measure["measure"]),
            "beat": float(musical_beat),
            "duration_beats": max(0.25, quantized_duration)
        })
        
    return quantized_notes