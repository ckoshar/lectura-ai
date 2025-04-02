import os
import subprocess
import shutil
import tempfile
import whisper

def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg is not installed or not found in system PATH.")

def get_notes_folder():
    notes_folder = os.path.join(os.path.expanduser("~"), "Lectura", "notes")
    os.makedirs(notes_folder, exist_ok=True)
    return notes_folder

def convert_to_wav(input_path):
    check_ffmpeg()
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav.close()

    command = [
        "ffmpeg",
        "-i", input_path,
        "-ar", "16000",  # Sample rate required by whisper
        "-ac", "1",      # Mono channel
        temp_wav.name,
        "-y"             # Overwrite output if exists
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return temp_wav.name

def transcribe(file_path):
    check_ffmpeg()

    # Get clean filename for saving transcript
    filename_base = os.path.splitext(os.path.basename(file_path))[0]
    transcript_path = os.path.join(get_notes_folder(), f"{filename_base}.txt")

    # Convert if necessary
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in [".mp3", ".wav"]:
        file_path = convert_to_wav(file_path)
        cleanup_temp = True
    else:
        cleanup_temp = False

    # Load and run Whisper
    model = whisper.load_model("base")
    result = model.transcribe(file_path, fp16=False)

    # Write transcript
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Clean up temp file if created
    if cleanup_temp and os.path.exists(file_path):
        os.remove(file_path)

    return transcript_path
