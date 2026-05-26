from music21 import *
import copy


class MidiPostProcessor:

    def __init__(self):

        self.quantization = 0.25

    # =====================================================
    # LOAD MIDI
    # =====================================================

    def load_score(self, midi_path):

        return converter.parse(midi_path)

    # =====================================================
    # REMOVE EXTREME NOTES
    # =====================================================

    def filter_notes(self, score):

        for part in score.parts:

            for n in list(part.recurse().notes):

                if isinstance(n, note.Note):

                    if n.pitch.midi < 21 or n.pitch.midi > 108:

                        n.activeSite.remove(n)

                elif isinstance(n, chord.Chord):

                    cleaned = []

                    for p in n.pitches:

                        if 21 <= p.midi <= 108:

                            cleaned.append(p)

                    if len(cleaned) == 0:

                        n.activeSite.remove(n)

                    else:

                        n.pitches = cleaned

        return score

    # =====================================================
    # QUANTIZATION
    # =====================================================

    def quantize(self, score):

        for n in score.recurse().notes:

            offset = round(
                n.offset / self.quantization
            ) * self.quantization

            duration = round(
                n.quarterLength / self.quantization
            ) * self.quantization
            try:    
                n.offset = max(0, offset)
            except:
                pass

            n.quarterLength = max(
                self.quantization,
                duration
            )

        return score

    # =====================================================
    # REMOVE TINY NOTES
    # =====================================================

    def remove_tiny_notes(self, score):

        for n in list(score.recurse().notes):

            if n.quarterLength < 0.25:

                n.activeSite.remove(n)

        return score

    # =====================================================
    # CHORD SIMPLIFICATION
    # =====================================================

    def simplify_chords(self, score):

        for c in score.recurse().getElementsByClass(
            chord.Chord
        ):

            unique = []

            seen = set()

            for p in c.pitches:

                if p.midi not in seen:

                    unique.append(p)

                    seen.add(p.midi)

            if len(unique) > 6:

                unique = unique[:6]

            c.pitches = unique

        return score

    # =====================================================
    # SPLIT HANDS
    # =====================================================

    def split_hands(self, score):

        right = stream.Part()
        left  = stream.Part()

        split_point = 60

        for n in score.recurse().notes:

            # Use absolute offset in the full score hierarchy
            # n.offset alone is relative to its immediate parent container
            # and resets to 0 when inserted into a new Part
            try:
                abs_offset = n.getOffsetInHierarchy(score)
            except Exception:
                abs_offset = n.offset

            if isinstance(n, note.Note):

                target = (
                    right
                    if n.pitch.midi >= split_point
                    else left
                )

                new_note = copy.deepcopy(n)

                target.insert(abs_offset, new_note)

            elif isinstance(n, chord.Chord):

                high = []
                low  = []

                for p in n.pitches:
                    if p.midi >= split_point:
                        high.append(p)
                    else:
                        low.append(p)

                if len(high) > 0:
                    right.insert(
                        abs_offset,
                        chord.Chord(high, quarterLength=n.quarterLength)
                    )

                if len(low) > 0:
                    left.insert(
                        abs_offset,
                        chord.Chord(low, quarterLength=n.quarterLength)
                    )

        final_score = stream.Score()
        final_score.insert(0, right)
        final_score.insert(0, left)

        return final_score

    # =====================================================
    # PROCESS PIPELINE
    # =====================================================

    def process(
        self,
        input_midi,
        output_midi
    ):

        score = self.load_score(
            input_midi
        )

        score = self.filter_notes(score)

        score = self.quantize(score)

        score = self.remove_tiny_notes(score)

        score = self.simplify_chords(score)

        score = self.split_hands(score)

        score.write(
            "midi",
            fp=output_midi
        )

        print(
            f"✅ Clean MIDI exported: {output_midi}"
        )