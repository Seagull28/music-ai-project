from faster_whisper import WhisperModel


class LyricsEngine:

    def __init__(
        self,
        device="cpu",
        model_size="small"
    ):

        compute_type = (
            "float16"
            if device == "cuda"
            else "int8"
        )

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe_audio(
        self,
        audio_path,
        language="en"
    ):
        segments, info = self.model.transcribe(
            audio_path,
            language=language
        )

        segments = list(segments)

        text = "\n".join(
            seg.text for seg in segments
        )

        return {
            "text": text,
            "segments": segments
        }