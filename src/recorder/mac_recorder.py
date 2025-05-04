import os
import subprocess
import time
import datetime
import shutil
from pathlib import Path
from error_handler import (
    RecordingError, 
    handle_error, 
    logger
)

def check_mac_permissions():
    """
    Check if the app has necessary permissions for audio recording.
    Returns True if permissions are granted, False otherwise.
    """
    try:
        # Check if we can access the microphone
        result = subprocess.run(
            ["osascript", "-e", "tell application \"System Events\" to tell process \"Terminal\" to get every window"],
            capture_output=True,
            text=True
        )
        return True
    except Exception as e:
        logger.warning(f"Permission check failed: {str(e)}")
        return False

def request_mac_permissions():
    """
    Request necessary permissions for audio recording.
    """
    logger.info("Requesting microphone permissions")
    print("⚠️ Lectura needs permission to access your microphone.")
    print("Please grant permission when prompted.")
    
    try:
        subprocess.run(
            ["osascript", "-e", "tell application \"System Events\" to tell process \"Terminal\" to get every window"],
            capture_output=True,
            text=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to request permissions: {str(e)}")
        return False

def start_recording(output_dir=None):
    """
    Start recording audio using macOS's built-in audio recording capabilities.
    
    Args:
        output_dir: Directory to save the recording (default: ~/Lectura/recordings)
        
    Returns:
        Path to the recording file
        
    Raises:
        RecordingError: If recording fails
    """
    try:
        # Check permissions
        if not check_mac_permissions():
            if not request_mac_permissions():
                raise RecordingError("Cannot access microphone. Please grant permission in System Preferences.")
        
        # Set up output directory
        if output_dir is None:
            home = os.path.expanduser("~")
            output_dir = os.path.join(home, "Lectura", "recordings")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"lecture_{timestamp}.m4a")
        
        logger.info(f"Starting recording to {output_file}")
        # Start recording using the 'rec' command (part of sox)
        # Note: This requires sox to be installed (brew install sox)
        try:
            print(f"🎤 Recording started. Press Ctrl+C to stop.")
            subprocess.run([
                "rec", 
                "-q", 
                "-c", "1",  # Mono
                "-r", "44100",  # Sample rate
                output_file
            ])
            print(f"✅ Recording saved to: {output_file}")
            logger.info(f"Recording completed successfully: {output_file}")
            return output_file
        except KeyboardInterrupt:
            print("\n⏹️ Recording stopped.")
            logger.info("Recording stopped by user")
            return output_file
        except Exception as e:
            logger.error(f"Error during recording: {str(e)}")
            raise RecordingError(f"Error during recording: {str(e)}")
    except RecordingError as e:
        # Re-raise recording errors
        raise
    except Exception as e:
        # Wrap other exceptions
        raise RecordingError(f"Unexpected error during recording: {str(e)}")

def check_sox_installation():
    """
    Check if sox is installed, and provide instructions if not.
    """
    if shutil.which("rec") is None:
        logger.warning("Sox is not installed")
        print("❌ Sox is not installed. Please install it with:")
        print("   brew install sox")
        return False
    logger.info("Sox is installed")
    return True

if __name__ == "__main__":
    if not check_sox_installation():
        exit(1)
    
    print("🎙️ Lectura Audio Recorder")
    print("------------------------")
    print("This will record audio from your microphone.")
    print("Press Ctrl+C to stop recording when you're done.")
    
    try:
        recording_path = start_recording()
        
        if recording_path:
            print(f"\n🎉 Recording complete!")
            print(f"📁 Saved to: {recording_path}")
            print("\nTo transcribe this recording, run:")
            print(f"python transcribe.py {recording_path}")
    except Exception as e:
        error_message = handle_error(e, "mac_recorder.py")
        print(f"Error: {error_message}")
        exit(1) 