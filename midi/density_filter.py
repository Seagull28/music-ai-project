from music21 import stream


class DensityFilter:

    def filter_notes(
        self,
        score,
        min_duration=0.1
    ):

        cleaned = stream.Score()

        for part in score.parts:

            new_part = stream.Part()

            for n in part.recurse().notes:

                if n.quarterLength >= min_duration:
                    new_part.append(n)

            cleaned.append(new_part)

        return cleaned