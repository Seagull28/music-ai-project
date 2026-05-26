from music21 import stream
from music21 import note
from music21 import chord


class HandSplitter:

    def split_hands(
        self,
        score,
        split_point=60
    ):

        right = stream.Part()
        left = stream.Part()

        for n in score.recurse().notes:

            # -------------------------
            # SINGLE NOTE
            # -------------------------
            if isinstance(n, note.Note):

                target = (
                    right
                    if n.pitch.midi >= split_point
                    else left
                )

                target.insert(
                    n.offset,
                    n
                )

            # -------------------------
            # CHORD
            # -------------------------
            elif isinstance(n, chord.Chord):

                avg_pitch = sum(
                    p.midi for p in n.pitches
                ) / len(n.pitches)

                target = (
                    right
                    if avg_pitch >= split_point
                    else left
                )

                target.insert(
                    n.offset,
                    n
                )

        final_score = stream.Score()

        final_score.insert(0, right)
        final_score.insert(0, left)

        return final_score