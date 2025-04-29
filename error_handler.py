import os
import sys
import traceback
import logging
from datetime import datetime

# Configure logging
def setup_logging(log_dir=None):
    """
    Set up logging configuration.
    
    Args:
        log_dir: Directory to store log files (default: ~/Lectura/logs)
    """
    if log_dir is None:
        home = os.path.expanduser("~")
        log_dir = os.path.join(home, "Lectura", "logs")
    
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"lectura_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger("Lectura")

# Initialize logger
logger = setup_logging()

class LecturaError(Exception):
    """Base exception class for Lectura."""
    pass

class TranscriptionError(LecturaError):
    """Exception raised for errors during transcription."""
    pass

class SummarizationError(LecturaError):
    """Exception raised for errors during summarization."""
    pass

class RecordingError(LecturaError):
    """Exception raised for errors during audio recording."""
    pass

class APIError(LecturaError):
    """Exception raised for API-related errors."""
    pass

class FileError(LecturaError):
    """Exception raised for file-related errors."""
    pass

def handle_error(error, context=None):
    """
    Centralized error handling function.
    
    Args:
        error: The exception that was raised
        context: Additional context about where the error occurred
        
    Returns:
        A user-friendly error message
    """
    # Log the error with full traceback
    if context:
        logger.error(f"Error in {context}: {str(error)}")
    else:
        logger.error(f"Error: {str(error)}")
    
    logger.debug(traceback.format_exc())
    
    # Generate user-friendly message based on error type
    if isinstance(error, TranscriptionError):
        return f"Transcription failed: {str(error)}"
    elif isinstance(error, SummarizationError):
        return f"Summarization failed: {str(error)}"
    elif isinstance(error, RecordingError):
        return f"Recording failed: {str(error)}"
    elif isinstance(error, APIError):
        return f"API error: {str(error)}"
    elif isinstance(error, FileError):
        return f"File error: {str(error)}"
    else:
        return f"An unexpected error occurred: {str(error)}"

def check_api_keys():
    """
    Check if required API keys are set.
    
    Returns:
        A list of missing API keys
    """
    missing_keys = []
    
    # Check Anthropic API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        missing_keys.append("ANTHROPIC_API_KEY")
    
    # Check Deepgram API key
    if not os.environ.get("DEEPGRAM_API_KEY"):
        missing_keys.append("DEEPGRAM_API_KEY")
    
    return missing_keys

def check_dependencies():
    """
    Check if required dependencies are installed.
    
    Returns:
        A list of missing dependencies
    """
    missing_deps = []
    
    # Check ffmpeg
    if not os.system("which ffmpeg > /dev/null 2>&1") == 0:
        missing_deps.append("ffmpeg")
    
    # Check sox
    if not os.system("which rec > /dev/null 2>&1") == 0:
        missing_deps.append("sox")
    
    return missing_deps 