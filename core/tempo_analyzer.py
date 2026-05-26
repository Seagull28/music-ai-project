import librosa


class TempoAnalyzer:

    def analyze(self, audio_path):

        y, sr = librosa.load(audio_path)

        tempo, beats = librosa.beat.beat_track(
            y=y,
            sr=sr
        )

        return {
            "tempo": round(float(tempo), 2),
            "time_signature": "4/4"
        }