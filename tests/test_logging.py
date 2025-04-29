import logging
import os
from pathlib import Path
from logging_config import setup_logging

def test_logging_setup():
    """Test that logging is properly configured."""
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
    log_file = Path.home() / ".lectura" / "logs" / "lectura.log"
    assert log_file.exists()
    
    # Test that root logger has correct handlers
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 2  # File and console handlers
    
    # Test logging levels
    assert root_logger.level == logging.DEBUG
    assert any(h.level == logging.DEBUG for h in root_logger.handlers)  # File handler
    assert any(h.level == logging.INFO for h in root_logger.handlers)   # Console handler 