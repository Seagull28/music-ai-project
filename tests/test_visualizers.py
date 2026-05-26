from visualizers.piano.piano_visualizer import generate_piano_visualizer


def test_visualizer():

    generate_piano_visualizer(
        "test.mid",
        "visualizer.html",
        "Test Song"
    )

    print("✅ Visualizer test passed")