import os
import sys
import argparse
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent))

from utils.logging_config import setup_logging
from utils.error_handler import handle_error
from transcribe import transcribe
from api.deepgram_transcribe import transcribe as deepgram_transcribe
from summary import append_summary_to_file

# Initialize logging
logger = setup_logging()

def main():
    """
    Main entry point for the Lectura application.
    """
    parser = argparse.ArgumentParser(description="Lectura - AI-powered lecture notes")
    parser.add_argument("--record", action="store_true", help="Start recording audio")
    parser.add_argument("--transcribe", type=str, help="Transcribe an audio file")
    parser.add_argument("--summarize", type=str, help="Summarize a transcript file")
    parser.add_argument("--deepgram", type=str, help="Transcribe using Deepgram")
    
    args = parser.parse_args()
    
    try:
        # Record audio
        if args.record:
            logger.info("Starting recording mode")
            from recorder.platform_detector import import_recorder
            recorder = import_recorder()
            recording_path = recorder.start_recording()
            
            if recording_path:
                print(f"\n🎉 Recording complete!")
                print(f"📁 Saved to: {recording_path}")
                print("\nTo transcribe this recording, run:")
                print(f"python app.py --transcribe {recording_path}")
        
        # Transcribe audio
        elif args.transcribe:
            logger.info(f"Starting transcription of {args.transcribe}")
            transcript_path = transcribe(args.transcribe)
            
            if transcript_path:
                print(f"\n🎉 Transcription complete!")
                print(f"📝 Transcript saved to: {transcript_path}")
                print("\nTo summarize this transcript, run:")
                print(f"python app.py --summarize {transcript_path}")
        
        # Summarize transcript
        elif args.summarize:
            logger.info(f"Starting summarization of {args.summarize}")
            append_summary_to_file(args.summarize)
            
            print(f"\n🎉 Summarization complete!")
            print(f"📝 Summary appended to: {args.summarize}")
        
        # Transcribe with Deepgram
        elif args.deepgram:
            logger.info(f"Starting Deepgram transcription of {args.deepgram}")
            transcript_path = deepgram_transcribe(args.deepgram)
            
            if transcript_path:
                print(f"\n🎉 Deepgram transcription complete!")
                print(f"📝 Transcript saved to: {transcript_path}")
                print("\nTo summarize this transcript, run:")
                print(f"python app.py --summarize {transcript_path}")
        
        else:
            parser.print_help()
            
    except Exception as e:
        error_message = handle_error(e, "app.py")
        print(f"Error: {error_message}")
        sys.exit(1)

if __name__ == "__main__":
    main() 