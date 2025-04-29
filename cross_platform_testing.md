# Cross-Platform Testing Guide for Lectura

## Current Platform Support

Lectura currently has the following platform support:

- **macOS**: Full support with native audio recording
- **Windows**: Partial support (transcription and summarization work, but recording needs adaptation)
- **Linux**: Partial support (transcription and summarization work, but recording needs adaptation)

## Testing Approaches

### 1. Virtual Machines

Set up virtual machines for each target platform:

- **Windows**: Use VirtualBox or VMware to run Windows 10/11
- **Linux**: Use VirtualBox or VMware to run Ubuntu, Fedora, or other distributions
- **macOS**: Already your primary development platform

### 2. Docker Containers

Create Docker containers for testing in isolated environments:

```bash
# Example Dockerfile for testing
FROM python:3.9-slim

WORKDIR /app
COPY . /app/

RUN apt-get update && apt-get install -y \
    ffmpeg \
    sox \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### 3. CI/CD Pipeline

Set up a continuous integration pipeline that tests on multiple platforms:

- GitHub Actions
- GitLab CI
- Jenkins

## Platform-Specific Adaptations Needed

### Windows

1. **Audio Recording**: Replace `mac_recorder.py` with a Windows-compatible version using:
   - PyAudio
   - SoundDevice
   - Windows Core Audio API

2. **Permission Handling**: Implement Windows-specific permission requests

### Linux

1. **Audio Recording**: Create a Linux-specific recorder using:
   - ALSA
   - PulseAudio
   - JACK

2. **Permission Handling**: Implement Linux-specific permission checks

## Testing Checklist

For each platform, verify:

1. **Dependencies Installation**:
   - Python packages
   - System dependencies (ffmpeg, sox, etc.)
   - API keys configuration

2. **Audio Recording**:
   - Permission requests
   - Recording quality
   - File saving

3. **Transcription**:
   - Whisper transcription
   - Deepgram transcription
   - File format compatibility

4. **Summarization**:
   - Claude API integration
   - Summary generation
   - File appending

5. **Error Handling**:
   - Proper error messages
   - Logging functionality
   - Recovery from errors

## Recommended Testing Tools

1. **Audio Testing**:
   - Audacity for audio file verification
   - Different microphone types and qualities

2. **Performance Testing**:
   - Memory usage monitoring
   - CPU utilization
   - Processing time for large files

3. **UI Testing** (when implemented):
   - Different screen resolutions
   - Different DPI settings
   - Accessibility testing 