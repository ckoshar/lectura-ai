import logging
import os
from pathlib import Path
from logging_config import setup_logging

def test_logging_setup():
    """Test that logging is properly configured."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Test log file path
    log_file = project_root / "data" / "logs" / "lectura.log"
    
    # Ensure the logs directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Test logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Test logging
    logger = logging.getLogger(__name__)
    logger.info("Test log message")
    
    # Verify log file was created
    assert log_file.exists()
    
    # Clean up
    if log_file.exists():
        log_file.unlink()

    # Set up logging
    loggers = setup_logging()
    
    # Test that all expected loggers are created
    assert 'recorder' in loggers
    assert 'transcriber' in loggers
    assert 'summarizer' in loggers
    assert 'api' in loggers
    
    # Test that loggers have correct names
    assert loggers['recorder'].name == 'lectura.recorder'
    assert loggers['transcriber'].name == 'lectura.transcriber'
    assert loggers['summarizer'].name == 'lectura.summarizer'
    assert loggers['api'].name == 'lectura.api'
    
    # Test that log file is created
    assert log_file.exists()
    
    # Test that root logger has correct handlers
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 2  # File and console handlers
    
    # Test logging levels
    assert root_logger.level == logging.DEBUG
    assert any(h.level == logging.DEBUG for h in root_logger.handlers)  # File handler
    assert any(h.level == logging.INFO for h in root_logger.handlers)   # Console handler 