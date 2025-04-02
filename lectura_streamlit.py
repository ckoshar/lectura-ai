import streamlit as st
from transcribe import transcribe
from summary import generate_summary
import os

st.set_page_config(page_title="Lectura", layout="centered")

st.title("🎧 Lectura – AI-Powered Lecture Notes")

uploaded_file = st.file_uploader(
    "Upload a lecture recording (.mp3, .m4a, .wav)",
    type=["mp3", "m4a", "wav"]
)

if uploaded_file is not None:
    with st.spinner("Processing your file... ⏳"):
        # Save to temporary file
        with open("temp_audio", "wb") as f:
            f.write(uploaded_file.read())

        # Transcribe
        transcript_path = transcribe("temp_audio")

        # Read transcript
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        # Generate summary
        summary = generate_summary(transcript)

    st.success("Done! Here's your output👇")

    st.subheader("📝 Transcript")
    st.text_area("Transcript", transcript, height=300)

    st.subheader("🧠 Summary + Study Tips")
    st.text(summary)
