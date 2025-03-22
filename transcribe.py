import os
from faster_whisper import WhisperModel
from pydub import AudioSegment

# Manually set FFmpeg path (replace with actual path from 'which ffmpeg')
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffprobe = "/opt/homebrew/bin/ffprobe"

def convert_m4a_to_wav(audio_path):
    """Converts an M4A file to WAV format."""
    wav_path = audio_path.replace(".m4a", ".wav")
    audio = AudioSegment.from_file(audio_path, format="m4a")
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_audio(audio_path):
    """Transcribes audio using Faster Whisper."""
    if audio_path.endswith(".m4a"):
        print("Converting .m4a to .wav...")
        audio_path = convert_m4a_to_wav(audio_path)

    model = WhisperModel("base")
    segments, info = model.transcribe(audio_path)

    transcription_text = " ".join(segment.text for segment in segments)
    return transcription_text

# Example usage
audio_file = "Acc_class.m4a"
transcription = transcribe_audio(audio_file)
print("Transcription:\n", transcription)
