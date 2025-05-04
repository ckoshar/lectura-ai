import os
import time
import datetime
import wave
import pyaudio
from pathlib import Path
from error_handler import (
    RecordingError, 
    handle_error, 
    logger
)

def check_windows_permissions():
    """
    Check if the app has necessary permissions for audio recording on Windows.
    Returns True if permissions are granted, False otherwise.
    """
    try:
        # On Windows, we'll try to initialize PyAudio to check permissions
        p = pyaudio.PyAudio()
        p.terminate()
        logger.info("Windows audio permissions verified")
        return True
    except Exception as e:
        logger.warning(f"Windows permission check failed: {str(e)}")
        return False

def request_windows_permissions():
    """
    Request necessary permissions for audio recording on Windows.
    """
    logger.info("Requesting Windows microphone permissions")
    print("⚠️ Lectura needs permission to access your microphone.")
    print("Please grant permission when prompted by Windows.")
    
    try:
        # On Windows, the system will automatically prompt for permissions
        # when we try to access the microphone
        p = pyaudio.PyAudio()
        p.terminate()
        logger.info("Windows microphone permissions granted")
        return True
    except Exception as e:
        logger.error(f"Failed to request Windows permissions: {str(e)}")
        return False

def start_recording(output_dir=None):
    """
    Start recording audio using PyAudio on Windows.
    
    Args:
        output_dir: Directory to save the recording (default: ~/Lectura/recordings)
        
    Returns:
        Path to the recording file
        
    Raises:
        RecordingError: If recording fails
    """
    try:
        # Check permissions
        if not check_windows_permissions():
            if not request_windows_permissions():
                raise RecordingError("Cannot access microphone. Please grant permission in Windows Settings.")
        
        # Set up output directory
        if output_dir is None:
            home = os.path.expanduser("~")
            output_dir = os.path.join(home, "Lectura", "recordings")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"lecture_{timestamp}.wav")
        
        logger.info(f"Starting recording to {output_file}")
        
        # Audio recording parameters
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # Open audio stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print(f"🎤 Recording started. Press Ctrl+C to stop.")
        
        # Record audio
        frames = []
        try:
            while True:
                data = stream.read(CHUNK)
                frames.append(data)
        except KeyboardInterrupt:
            print("\n⏹️ Recording stopped.")
            logger.info("Recording stopped by user")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save the recorded data as a WAV file
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"✅ Recording saved to: {output_file}")
        logger.info(f"Recording completed successfully: {output_file}")
        return output_file
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
    try:
        import pyaudio
        logger.info("PyAudio is installed")
        return True
    except ImportError:
        logger.warning("PyAudio is not installed")
        print("❌ PyAudio is not installed. Please install it with:")
        print("   pip install pyaudio")
        print("\nIf that fails, you may need to install PortAudio first:")
        print("   Windows: Download and install from https://www.portaudio.com/download.html")
        print("   Linux: sudo apt-get install python3-pyaudio")
        print("   macOS: brew install portaudio")
        return False

if __name__ == "__main__":
    if not check_dependencies():
        exit(1)
    
    print("🎙️ Lectura Audio Recorder (Windows)")
    print("----------------------------------")
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
        error_message = handle_error(e, "windows_recorder.py")
        print(f"Error: {error_message}")
        exit(1) 