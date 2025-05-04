from dataclasses import dataclass
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RECORDINGS_DIR = DATA_DIR / "recordings"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
SUMMARIES_DIR = DATA_DIR / "summaries"
LOGS_DIR = DATA_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, RECORDINGS_DIR, TRANSCRIPTS_DIR, SUMMARIES_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Model configurations
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"
T5_MODEL = "t5-small"  # Options: "t5-small", "t5-base", "t5-large"

# Recording settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
RECORD_SECONDS = 300  # Default recording duration in seconds

@dataclass
class APIConfig:
    anthropic_api_key: str
    deepgram_api_key: str

@dataclass
class StorageConfig:
    recordings_dir: Path
    transcripts_dir: Path
    summaries_dir: Path

@dataclass
class RecordingConfig:
    sample_rate: int = 44100
    channels: int = 1
    chunk_size: int = 1024
    format: str = "wav"

@dataclass
class Config:
    api: APIConfig
    storage: StorageConfig
    recording: RecordingConfig = RecordingConfig()

    @classmethod
    def from_env(cls) -> 'Config':
        # Validate required environment variables
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        if not deepgram_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is required")

        # Create base directories
        base_dir = Path.home() / ".lectura"
        recordings_dir = base_dir / "recordings"
        transcripts_dir = base_dir / "transcripts"
        summaries_dir = base_dir / "summaries"

        # Ensure directories exist
        for directory in [recordings_dir, transcripts_dir, summaries_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        return cls(
            api=APIConfig(
                anthropic_api_key=anthropic_key,
                deepgram_api_key=deepgram_key
            ),
            storage=StorageConfig(
                recordings_dir=recordings_dir,
                transcripts_dir=transcripts_dir,
                summaries_dir=summaries_dir
            )
        )

# Create a global config instance
config = Config.from_env() 