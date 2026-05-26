# subtitle_exporter.py

def format_time(seconds):

    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def export_srt(segments, output_path):

    with open(output_path, "w", encoding="utf-8") as f:

        for i, seg in enumerate(segments, start=1):

            start = format_time(seg.start)
            end = format_time(seg.end)

            text = seg.text.strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")