import os
import time
import datetime
import subprocess
import shutil
from pathlib import Path
from error_handler import (
    RecordingError, 
    handle_error, 
    logger
)

def check_linux_permissions():
    """
    Check if the app has necessary permissions for audio recording on Linux.
    Returns True if permissions are granted, False otherwise.
    """
    try:
        # Check if we can access audio devices
        # This is a simplified check - in a real app, you'd need more robust checks
        result = subprocess.run(
            ["arecord", "-l"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Linux audio permissions verified")
            return True
        else:
            logger.warning("Linux audio permission check failed")
            return False
    except Exception as e:
        logger.warning(f"Linux permission check failed: {str(e)}")
        return False

def request_linux_permissions():
    """
    Request necessary permissions for audio recording on Linux.
    """
    logger.info("Requesting Linux microphone permissions")
    print("⚠️ Lectura needs permission to access your microphone.")
    print("On Linux, you may need to add your user to the 'audio' group:")
    print("   sudo usermod -a -G audio $USER")
    print("Then log out and log back in for changes to take effect.")
    
    try:
        # Try to access audio device to trigger permission prompt
        result = subprocess.run(
            ["arecord", "-d", "1", "-f", "cd", "/dev/null"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Linux microphone permissions granted")
            return True
        else:
            logger.error("Failed to request Linux permissions")
            return False
    except Exception as e:
        logger.error(f"Failed to request Linux permissions: {str(e)}")
        return False

def start_recording(output_dir=None):
    """
    Start recording audio using ALSA on Linux.
    
    Args:
        output_dir: Directory to save the recording (default: ~/Lectura/recordings)
        
    Returns:
        Path to the recording file
        
    Raises:
        RecordingError: If recording fails
    """
    try:
        # Check permissions
        if not check_linux_permissions():
            if not request_linux_permissions():
                raise RecordingError("Cannot access microphone. Please check your Linux audio permissions.")
        
        # Set up output directory
        if output_dir is None:
            home = os.path.expanduser("~")
            output_dir = os.path.join(home, "Lectura", "recordings")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"lecture_{timestamp}.wav")
        
        logger.info(f"Starting recording to {output_file}")
        
        # Start recording using arecord (ALSA)
        print(f"🎤 Recording started. Press Ctrl+C to stop.")
        try:
            subprocess.run([
                "arecord",
                "-f", "cd",  # CD quality
                "-c", "1",   # Mono
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

def check_dependencies():
    """
    Check if required dependencies are installed.
    """
    if shutil.which("arecord") is None:
        logger.warning("ALSA utilities are not installed")
        print("❌ ALSA utilities are not installed. Please install them with:")
        print("   Ubuntu/Debian: sudo apt-get install alsa-utils")
        print("   Fedora: sudo dnf install alsa-utils")
        print("   Arch Linux: sudo pacman -S alsa-utils")
        return False
    logger.info("ALSA utilities are installed")
    return True

if __name__ == "__main__":
    if not check_dependencies():
        exit(1)
    
    print("🎙️ Lectura Audio Recorder (Linux)")
    print("--------------------------------")
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
        error_message = handle_error(e, "linux_recorder.py")
        print(f"Error: {error_message}")
        exit(1) 