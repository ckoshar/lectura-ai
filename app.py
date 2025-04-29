import os
import sys
import argparse
from error_handler import handle_error, logger
from platform_detector import import_recorder

def main():
    """
    Main entry point for the Lectura application.
    """
    parser = argparse.ArgumentParser(description="Lectura - AI-powered lecture notes")
    parser.add_argument("--record", action="store_true", help="Record audio from microphone")
    parser.add_argument("--transcribe", metavar="FILE", help="Transcribe an audio file")
    parser.add_argument("--summarize", metavar="FILE", help="Summarize a transcript file")
    parser.add_argument("--deepgram", metavar="FILE", help="Transcribe using Deepgram API")
    
    args = parser.parse_args()
    
    try:
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            return
        
        # Record audio
        if args.record:
            logger.info("Starting recording mode")
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
            from transcribe import transcribe
            transcript_path = transcribe(args.transcribe)
            
            if transcript_path:
                print(f"\n🎉 Transcription complete!")
                print(f"📝 Transcript saved to: {transcript_path}")
                print("\nTo summarize this transcript, run:")
                print(f"python app.py --summarize {transcript_path}")
        
        # Summarize transcript
        elif args.summarize:
            logger.info(f"Starting summarization of {args.summarize}")
            from summary import append_summary_to_file
            append_summary_to_file(args.summarize)
            
            print(f"\n🎉 Summarization complete!")
            print(f"📝 Summary appended to: {args.summarize}")
        
        # Transcribe with Deepgram
        elif args.deepgram:
            logger.info(f"Starting Deepgram transcription of {args.deepgram}")
            from deepgram_transcribe import transcribe
            transcript_path = transcribe(args.deepgram)
            
            if transcript_path:
                print(f"\n🎉 Deepgram transcription complete!")
                print(f"📝 Transcript saved to: {transcript_path}")
                print("\nTo summarize this transcript, run:")
                print(f"python app.py --summarize {transcript_path}")
    
    except Exception as e:
        error_message = handle_error(e, "app.py")
        print(f"Error: {error_message}")
        sys.exit(1)

if __name__ == "__main__":
    main() 