# AutoShorts Generator

Automatically generate viral-worthy YouTube Shorts from long-form videos. This tool downloads YouTube videos, detects engaging highlights, and creates vertical format clips with styled captions.

## Features

- Downloads YouTube videos using yt-dlp
- Transcribes audio using OpenAI Whisper
- Detects engaging segments using custom highlight detection
- Converts clips to vertical 9:16 format
- Adds MrBeast-style captions
- Exports multiple shorts from a single video

## Requirements

- Python 3.10+
- ffmpeg installed on your system
- Mac M1/Intel compatible

## Installation

1. Install ffmpeg:
```bash
# On macOS using Homebrew
brew install ffmpeg
```

2. Set up Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Specify maximum number of clips:
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --max-clips 4
```

## Output Structure

The tool creates several directories:
- `input/`: Downloaded YouTube videos
- `audio/`: Extracted audio files
- `transcripts/`: Video transcriptions
- `clips/`: Raw video clips
- `output/`: Final shorts with captions

## How It Works

1. Downloads the YouTube video using yt-dlp
2. Extracts audio for transcription
3. Transcribes audio using Whisper
4. Analyzes transcript to find engaging segments
5. Clips and formats videos to vertical format
6. Adds styled captions
7. Exports final shorts

## Highlight Detection

The system detects engaging segments based on:
- Keyword triggers (e.g., "incredible", "insane", "million")
- Sentence structure and length
- Emotional tone
- Natural segment boundaries

## Additional Notes

- Videos are formatted to 1080x1920 (9:16 aspect ratio)
- Each short is limited to 60 seconds max
- Captions are styled with white text and black stroke
- Processing time depends on video length and system specs