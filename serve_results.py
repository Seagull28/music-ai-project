import os
import sys
import webbrowser
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8000


class SilentHandler(SimpleHTTPRequestHandler):
    """Serve with CORS headers — required for audio + JS loading from localhost."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        # Only log errors (4xx/5xx), suppress routine GET noise
        if args and str(args[1]).startswith(('4', '5')):
            print(f"  ⚠️  [{args[1]}] {args[0]}")


def serve(song_name=None):
    output_dir = Path("output")

    if not output_dir.exists():
        print("❌ No 'output' folder found. Run the pipeline first.")
        sys.exit(1)

    abs_output = output_dir.resolve()
    os.chdir(output_dir)

    # Find the HTML sheet to open
    if song_name:
        sheets = list(Path(song_name).glob("sheets/*.html"))
        open_url = f"http://localhost:{PORT}/{song_name}/sheets/{sheets[0].name}" if sheets else f"http://localhost:{PORT}"
    else:
        songs = sorted(
            [d for d in Path(".").iterdir() if d.is_dir()],
            key=lambda d: d.stat().st_mtime,
            reverse=True,
        )
        if songs:
            sheets = list(songs[0].glob("sheets/*.html"))
            open_url = (
                f"http://localhost:{PORT}/{songs[0].name}/sheets/{sheets[0].name}"
                if sheets else f"http://localhost:{PORT}"
            )
        else:
            open_url = f"http://localhost:{PORT}"

    server = HTTPServer(("localhost", PORT), SilentHandler)

    print(f"\n🌐 Serving output at : http://localhost:{PORT}")
    print(f"🎹 Opening sheet     : {open_url}")
    print(f"📂 Serving from      : {abs_output}")
    print(f"\n  ⚠️  Always use http://localhost:{PORT} — never open HTML with file://")
    print(f"  Press Ctrl+C to stop\n")

    webbrowser.open(open_url)
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve Music AI pipeline output")
    parser.add_argument(
        "song", nargs="?", default=None,
        help="Song name to open (e.g. test). Auto-detects latest if omitted."
    )
    args = parser.parse_args()
    serve(args.song)