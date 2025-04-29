import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import config

def setup_logging():
    """Configure logging for the application."""
    # Create logs directory
    log_dir = Path.home() / ".lectura" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        log_dir / "lectura.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Create loggers for different components
    loggers = {
        'recorder': logging.getLogger('lectura.recorder'),
        'transcriber': logging.getLogger('lectura.transcriber'),
        'summarizer': logging.getLogger('lectura.summarizer'),
        'api': logging.getLogger('lectura.api')
    }
    
    return loggers

# Initialize logging
loggers = setup_logging() 