import os
import subprocess
import shutil
import tempfile
import whisper
from error_handler import (
    TranscriptionError, 
    FileError, 
    handle_error, 
    logger
)

def check_ffmpeg():
    """Check if ffmpeg is installed."""
    if shutil.which("ffmpeg") is None:
        raise TranscriptionError("ffmpeg is not installed or not found in system PATH.")

def get_notes_folder():
    """Get the folder where transcripts are saved."""
    notes_folder = os.path.join(os.path.expanduser("~"), "Lectura", "notes")
    os.makedirs(notes_folder, exist_ok=True)
    return notes_folder

def convert_to_wav(input_path):
    """
    Convert audio file to WAV format.
    
    Args:
        input_path: Path to the input audio file
        
    Returns:
        Path to the converted WAV file
    """
    try:
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
    except subprocess.CalledProcessError as e:
        raise TranscriptionError(f"Failed to convert audio to WAV: {str(e)}")
    except Exception as e:
        raise TranscriptionError(f"Unexpected error during audio conversion: {str(e)}")

def transcribe(file_path):
    """
    Transcribe an audio file using Whisper.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Path to the transcript file
    """
    try:
        logger.info(f"Starting transcription of {file_path}")
        check_ffmpeg()

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileError(f"File not found: {file_path}")

        # Get clean filename for saving transcript
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        transcript_path = os.path.join(get_notes_folder(), f"{filename_base}.txt")

        # Convert if necessary
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".mp3", ".wav"]:
            logger.info(f"Converting {file_path} to WAV format")
            file_path = convert_to_wav(file_path)
            cleanup_temp = True
        else:
            cleanup_temp = False

        # Load and run Whisper
        logger.info("Loading Whisper model")
        model = whisper.load_model("base")
        
        logger.info("Transcribing audio")
        result = model.transcribe(file_path, fp16=False)

        # Write transcript
        logger.info(f"Writing transcript to {transcript_path}")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        # Clean up temp file if created
        if cleanup_temp and os.path.exists(file_path):
            os.remove(file_path)

        logger.info("Transcription completed successfully")
        return transcript_path
    except TranscriptionError as e:
        # Re-raise custom exceptions
        raise
    except Exception as e:
        # Wrap other exceptions
        raise TranscriptionError(f"Transcription failed: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        transcript_path = transcribe(file_path)
        print(f"Transcript saved to: {transcript_path}")
    except Exception as e:
        error_message = handle_error(e, "transcribe.py")
        print(f"Error: {error_message}")
        sys.exit(1)
