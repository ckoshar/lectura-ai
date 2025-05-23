import os
import asyncio
from pathlib import Path
from deepgram import DeepgramClient, PrerecordedOptions
from utils.error_handler import (
    TranscriptionError, 
    APIError, 
    FileError, 
    handle_error, 
    logger
)
from config import TRANSCRIPTS_DIR

# Initialize Deepgram client
try:
    dg_client = DeepgramClient(os.environ.get("DEEPGRAM_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize Deepgram client: {str(e)}")
    dg_client = None

def get_data_dir():
    """Get the data directory where transcripts are saved."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

async def transcribe_with_deepgram(file_path):
    """
    Transcribe an audio file using Deepgram's API.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Path to the transcript file
    """
    # Check if client is initialized
    if dg_client is None:
        raise APIError("Deepgram client not initialized. Please set DEEPGRAM_API_KEY environment variable.")
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileError(f"File not found: {file_path}")
    
    try:
        # Get clean filename for saving transcript
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        transcript_path = TRANSCRIPTS_DIR / f"{filename_base}_deepgram.txt"
        
        logger.info(f"Opening audio file: {file_path}")
        # Open the audio file
        with open(file_path, 'rb') as audio:
            # Set transcription options
            options = PrerecordedOptions(
                smart_format=True,
                model="nova-2",
                language="en-US",
                punctuate=True,
                diarize=True,  # Speaker identification
                utterances=True,
            )
            
            logger.info("Sending request to Deepgram")
            # Send request to Deepgram
            response = await dg_client.listen.prerecorded.v("1").transcribe_file(audio, options)
            
            logger.info("Extracting transcript from response")
            # Extract transcript
            transcript = response.results.channels[0].alternatives[0].transcript
            
            logger.info(f"Writing transcript to {transcript_path}")
            # Write transcript to file
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
                
            logger.info("Transcription completed successfully")
            return str(transcript_path)
    except Exception as e:
        logger.error(f"Deepgram transcription failed: {str(e)}")
        raise TranscriptionError(f"Deepgram transcription failed: {str(e)}")

def transcribe(file_path):
    """
    Synchronous wrapper for the async transcribe function.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Path to the transcript file
    """
    try:
        return asyncio.run(transcribe_with_deepgram(file_path))
    except Exception as e:
        if isinstance(e, TranscriptionError):
            raise
        else:
            raise TranscriptionError(f"Unexpected error during transcription: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python deepgram_transcribe.py <audio_file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        transcript_path = transcribe(file_path)
        print(f"Transcript saved to: {transcript_path}")
    except Exception as e:
        error_message = handle_error(e, "deepgram_transcribe.py")
        print(f"Error: {error_message}")
        sys.exit(1) 