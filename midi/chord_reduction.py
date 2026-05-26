from music21 import chord


class ChordReducer:

    def reduce(self, score, max_notes=4):

        for c in score.recurse().getElementsByClass(chord.Chord):

            if len(c.pitches) > max_notes:

                reduced = c.pitches[:max_notes]

                c.pitches = reduced

        return score