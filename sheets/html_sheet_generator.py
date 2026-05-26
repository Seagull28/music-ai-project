import json
import os

def generate_html_sheet(
    musicxml_path,
    output_html,
    song_name,
    instrument,
    audio_path,
    midi_path,
    timeline_data_json_str
):
    # 1. Safely handle the json payload without crashing
    if isinstance(timeline_data_json_str, str) and timeline_data_json_str.strip().startswith('{'):
        final_json_payload = timeline_data_json_str
    elif timeline_data_json_str and os.path.exists(str(timeline_data_json_str)):
        with open(timeline_data_json_str, "r", encoding="utf-8") as f:
            final_json_payload = f.read()
    else:
        final_json_payload = '{"notes":[]}'

    # stem_separator.py passes cleaned.wav to demucs
    # demucs saves to: output/{song_name}/stems/htdemucs/cleaned/no_vocals.wav
    # serve_results.py serves from output/ as root → URL is /{song_name}/stems/...
    audio_rel_url = f"/{song_name}/stems/htdemucs/cleaned/no_vocals.wav"
    instrument_name = str(instrument).upper()

    # 3. Write out the code pieces carefully to avoid syntax or brace errors
    part_1_header = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{song_name} — MUX_AI Canvas</title>
    <style>
        body {{
            background-color: #0b0c10;
            color: #c5c6c7;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 30px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: #46a29f;
            margin-bottom: 5px;
            font-weight: 300;
            letter-spacing: 2px;
        }}
        .subtitle {{
            color: #66fcf1;
            margin-bottom: 25px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .player-panel {{
            background: #1f2833;
            padding: 15px 35px;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            margin-bottom: 35px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        audio {{
            filter: invert(90%) hue-rotate(180deg);
            outline: none;
        }}
        .status-mon {{
            font-size: 12px;
            color: #66fcf1;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
        }}
        .piano-scroll-frame {{
            background: #111111;
            padding: 20px;
            border-radius: 12px;
            box-shadow: inset 0 0 20px #000, 0 10px 40px rgba(0,0,0,0.8);
            width: 100%;
            max-width: 1300px;
            overflow-x: auto;
            margin-bottom: 20px;
        }}
        #piano-bed {{
            position: relative;
            display: block;
            height: 180px;
            width: 1248px;
            background: #000;
            user-select: none;
            margin: 0 auto;
            border: 4px solid #1f2833;
            border-radius: 4px;
        }}
        .key-unit {{
            position: absolute;
            width: 24px;
            height: 100%;
            background: linear-gradient(to bottom, #ffffff 0%, #ebebeb 100%);
            border: 1px solid #111;
            border-radius: 0 0 4px 4px;
            box-sizing: border-box;
            z-index: 1;
        }}
        .key-unit.sharp-flat {{
            width: 14px;
            height: 62%;
            background: linear-gradient(to bottom, #111111 0%, #333333 100%);
            border: 1px solid #000;
            border-radius: 0 0 3px 3px;
            z-index: 5;
            margin-left: -7px; 
        }}
        .key-unit.active-hit {{
            background: linear-gradient(to bottom, #66fcf1 0%, #46a29f 100%) !important;
            box-shadow: 0 0 15px #66fcf1, inset 0 0 4px #fff;
        }}
        .key-unit.sharp-flat.active-hit {{
            background: linear-gradient(to bottom, #66fcf1 0%, #1a252f 100%) !important;
            box-shadow: 0 0 15px #66fcf1;
        }}
    </style>
</head>
<body>

    <h1>{song_name}</h1>
    <div class="subtitle">MUX_AI Core — Interactive {instrument_name} Bed Visualizer</div>

    <div class="player-panel">
        <audio id="main-audio" controls>
            <source src="{audio_rel_url}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        <div class="status-mon" id="playback-time">TIME: 0.00s</div>
        <div class="status-mon" id="debug-info" style="font-size:10px; color:#46a29f; margin-left:10px;"></div>
    </div>

    <script>
    // Audio load error handler — shows actual path for debugging
    document.getElementById('main-audio').addEventListener('error', function() {{
        document.getElementById('playback-time').innerText = '⚠ Audio not found: {audio_rel_url}';
        console.error('Audio failed to load:', '{audio_rel_url}');
    }});
    </script>

    <div class="piano-scroll-frame">
        <div id="piano-bed"></div>
    </div>

<script>
"""

    # Pure JavaScript payload script string without confusing Python f-string bracket escaping
    part_2_javascript = f"""
    const timelineData = {final_json_payload};
    const noteArray = timelineData.notes || [];

    const pianoBed = document.getElementById('piano-bed');
    const audioTrack = document.getElementById('main-audio');
    const displayTime = document.getElementById('playback-time');
    const debugInfo  = document.getElementById('debug-info');

    // Show note count on load so we know data arrived
    if (debugInfo) {{
        debugInfo.innerText = `NOTES LOADED: ${{noteArray.length}}`;
    }}

    function checkBlackKey(midiNumber) {{
        const noteRemainder = midiNumber % 12;
        return [1, 3, 6, 8, 10].includes(noteRemainder);
    }}

    const elementsMap = {{}};
    let whiteIndex = 0;
    const WHITE_KEY_WIDTH = 24;

    for (let midi = 21; midi <= 108; midi++) {{
        const keyDiv = document.createElement('div');
        keyDiv.id = 'midi_' + midi;
        
        if (checkBlackKey(midi)) {{
            keyDiv.className = 'key-unit sharp-flat';
            keyDiv.style.left = (whiteIndex * WHITE_KEY_WIDTH) + 'px';
            pianoBed.appendChild(keyDiv);
        }} else {{
            keyDiv.className = 'key-unit white-natural';
            keyDiv.style.left = (whiteIndex * WHITE_KEY_WIDTH) + 'px';
            pianoBed.appendChild(keyDiv);
            whiteIndex++;
        }}
        elementsMap[midi] = keyDiv;
    }}

    function processFrame() {{
        const currentSecs = audioTrack.currentTime;
        
        let bpmString = timelineData.bpm ? " | BPM: " + timelineData.bpm : "";
        displayTime.innerText = "TIME: " + currentSecs.toFixed(2) + "s" + bpmString;

        for (let m in elementsMap) {{
            elementsMap[m].classList.remove('active-hit');
        }}

        let activeCount = 0;
        for (let i = 0; i < noteArray.length; i++) {{
            const activeNote = noteArray[i];
            if (currentSecs >= activeNote.start && currentSecs <= activeNote.end) {{
                const targetKey = elementsMap[activeNote.pitch];
                if (targetKey) {{
                    targetKey.classList.add('active-hit');
                    activeCount++;
                }}
            }}
        }}

        if (debugInfo) {{
            debugInfo.innerText = `NOTES: ${{noteArray.length}} | ACTIVE: ${{activeCount}}`;
        }}

        requestAnimationFrame(processFrame);
    }}

    requestAnimationFrame(processFrame);
</script>
</body>
</html>
"""

    # Combined write out
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(part_1_header + part_2_javascript)
    print(f"   └─ HTML Clean Audio Sync Complete: {output_html}")