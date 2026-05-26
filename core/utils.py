import os
import json


def ensure_directory(path):

    os.makedirs(path, exist_ok=True)


def save_json(data, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_song_name(audio_path):

    return os.path.splitext(
        os.path.basename(audio_path)
    )[0]