class RhythmQuantizer:

    def quantize(
        self,
        score,
        grid=0.25
    ):

        for n in score.recurse().notes:

            n.offset = round(n.offset / grid) * grid

        return score