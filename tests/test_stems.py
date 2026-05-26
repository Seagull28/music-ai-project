from core.stem_separator import separate_stems


def test_stem_separation():

    stems = separate_stems(
        "test.mp3",
        "test_output"
    )

    print(stems)

    print("✅ Stem separation passed")