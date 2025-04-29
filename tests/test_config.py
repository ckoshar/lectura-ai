import os
import pytest
from pathlib import Path
from config import Config, APIConfig, StorageConfig

def test_config_creation():
    """Test that Config can be created with valid environment variables."""
    # Set up test environment variables
    os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"
    os.environ["DEEPGRAM_API_KEY"] = "test_deepgram_key"
    
    config = Config.from_env()
    
    # Test API config
    assert isinstance(config.api, APIConfig)
    assert config.api.anthropic_api_key == "test_anthropic_key"
    assert config.api.deepgram_api_key == "test_deepgram_key"
    
    # Test storage config
    assert isinstance(config.storage, StorageConfig)
    assert isinstance(config.storage.recordings_dir, Path)
    assert isinstance(config.storage.transcripts_dir, Path)
    assert isinstance(config.storage.summaries_dir, Path)
    
    # Test recording config defaults
    assert config.recording.sample_rate == 44100
    assert config.recording.channels == 1
    assert config.recording.chunk_size == 1024
    assert config.recording.format == "wav"

def test_config_missing_env_vars():
    """Test that Config raises appropriate errors with missing environment variables."""
    # Clear environment variables
    if "ANTHROPIC_API_KEY" in os.environ:
        del os.environ["ANTHROPIC_API_KEY"]
    if "DEEPGRAM_API_KEY" in os.environ:
        del os.environ["DEEPGRAM_API_KEY"]
    
    # Test missing Anthropic API key
    os.environ["DEEPGRAM_API_KEY"] = "test_deepgram_key"
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        Config.from_env()
    
    # Test missing Deepgram API key
    del os.environ["DEEPGRAM_API_KEY"]
    os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"
    with pytest.raises(ValueError, match="DEEPGRAM_API_KEY"):
        Config.from_env() 