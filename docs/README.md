# Lectura - AI-Powered Lecture Notes

Lectura is an AI-powered application that helps you capture, transcribe, and summarize lecture content. It uses state-of-the-art AI models to generate accurate transcripts and insightful summaries of your lectures.

## Features

- **Audio Recording**: Record lectures directly from your microphone
- **Transcription**: Convert audio to text using OpenAI's Whisper or Deepgram
- **Summarization**: Generate concise summaries using Claude Sonnet 3.7
- **Cross-Platform**: Works on macOS, Windows, and Linux

## Installation

### Prerequisites

- Python 3.9 or higher
- FFmpeg (for audio processing)
- Sox (for macOS recording) or ALSA (for Linux) or PyAudio (for Windows)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lectura.git
   cd lectura
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:
   Create a `.env` file in the project root with:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ```

### Platform-Specific Setup

#### macOS
```bash
brew install ffmpeg sox
```

#### Windows
```bash
# Install FFmpeg from https://ffmpeg.org/download.html
# PyAudio will be installed via pip
```

#### Linux
```bash
sudo apt-get install ffmpeg alsa-utils
```

## Usage

Lectura can be used in two ways:

### Command Line Interface

```bash
# Record audio
python app.py --record

# Transcribe audio file
python app.py --transcribe path/to/audio.mp3

# Summarize transcript
python app.py --summarize path/to/transcript.txt

# Transcribe using Deepgram
python app.py --deepgram path/to/audio.mp3
```

### Web Interface

```bash
streamlit run streamlit_app.py
```

## How It Works

1. **Recording**: Capture audio from your microphone
2. **Transcription**: Convert audio to text using AI
3. **Summarization**: Generate a concise summary with key points
4. **Storage**: Save everything in an organized folder structure

## Project Structure

- `app.py`: Main entry point with CLI
- `streamlit_app.py`: Web interface
- `transcribe.py`: Whisper transcription
- `deepgram_transcribe.py`: Deepgram transcription
- `summary.py`: Claude summarization
- `mac_recorder.py`: macOS audio recording
- `windows_recorder.py`: Windows audio recording
- `linux_recorder.py`: Linux audio recording
- `platform_detector.py`: Platform detection
- `error_handler.py`: Error handling and logging

## Cross-Platform Support

Lectura is designed to work across multiple platforms:

- **macOS**: Uses Sox for audio recording
- **Windows**: Uses PyAudio for audio recording
- **Linux**: Uses ALSA for audio recording

The application automatically detects your platform and uses the appropriate recording method.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI Whisper for transcription
- Anthropic Claude for summarization
- Deepgram for alternative transcription
