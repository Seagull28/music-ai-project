import streamlit as st
import os
import subprocess
import shutil

st.set_page_config(
    page_title="MUX_AI",
    layout="wide"
)

st.title("🎵 MUX_AI")
st.subheader("AI Music Sheet + Piano Visualizer Generator")

uploaded = st.file_uploader(
    "Upload Audio",
    type=["mp3", "wav"]
)

instrument = st.selectbox(
    "Instrument",
    ["piano"]
)

if uploaded:

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    audio_path = os.path.join(
        temp_dir,
        uploaded.name
    )

    with open(audio_path, "wb") as f:
        f.write(uploaded.read())

    st.audio(audio_path)

    if st.button("Generate"):

        with st.spinner("Running MUX_AI Pipeline..."):

            cmd = [
                "python",
                "run_pipeline.py",
                audio_path,
                "--instrument",
                instrument
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

        st.text(result.stdout)

        if result.returncode != 0:

            st.error(result.stderr)

        else:

            song_name = os.path.splitext(
                uploaded.name
            )[0]

            output_dir = os.path.join(
                "output",
                song_name
            )

            html_sheet = os.path.join(
                output_dir,
                "sheets",
                f"{instrument}_sheet.html"
            )

            lyrics_txt = os.path.join(
                output_dir,
                "lyrics",
                "lyrics.txt"
            )

            midi_file = os.path.join(
                output_dir,
                "midi",
                f"{instrument}_arrangement.mid"
            )

            st.success("Pipeline Complete")

            if os.path.exists(lyrics_txt):

                st.subheader("Lyrics")

                with open(
                    lyrics_txt,
                    "r",
                    encoding="utf-8"
                ) as f:

                    st.text(f.read())

            if os.path.exists(midi_file):

                st.subheader("MIDI File")

                with open(midi_file, "rb") as f:

                    st.download_button(
                        "Download MIDI",
                        f,
                        file_name=os.path.basename(midi_file)
                    )

            if os.path.exists(html_sheet):

                st.subheader("Interactive Piano Visualizer")

                with open(
                    html_sheet,
                    "r",
                    encoding="utf-8"
                ) as f:

                    html_content = f.read()

                st.components.v1.html(
                    html_content,
                    height=900,
                    scrolling=True
                )