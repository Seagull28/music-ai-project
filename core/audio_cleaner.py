from pydub import AudioSegment


def clean_audio(input_audio, output_audio):

    audio = AudioSegment.from_file(input_audio)

    audio = audio.normalize()

    audio.export(output_audio, format="wav")