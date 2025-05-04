import os
import logging
import traceback
from pathlib import Path

def get_log_dir():
    """Get the directory for log files."""
    log_dir = Path(__file__).parent.parent.parent / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def setup_logger():
    """Set up the logger for the application."""
    # Create logs directory
    log_dir = get_log_dir()
    
    # Create logger
    logger = logging.getLogger("Lectura")
    logger.setLevel(logging.DEBUG)
    
    # Create file handler
    log_file = log_dir / "lectura.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

class LecturaError(Exception):
    """Base exception class for Lectura."""
    pass

class TranscriptionError(LecturaError):
    """Exception raised for transcription errors."""
    pass

class SummarizationError(LecturaError):
    """Exception raised for summarization errors."""
    pass

class RecordingError(LecturaError):
    """Exception raised for recording errors."""
    pass

class APIError(LecturaError):
    """Exception raised for API errors."""
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