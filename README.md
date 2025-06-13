# YouTube Video Summarizer

A Python application that downloads YouTube videos, extracts audio, and generates summaries using speech-to-text and text summarization technologies.

## Features

- Download YouTube videos
- Extract audio from video files
- Convert speech to text
- Generate concise summaries
- Simple command-line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Mayankmn143/youtube-video-summarizer.git
cd youtube-video-summarizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python summarizer.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Dependencies

- yt-dlp: For downloading YouTube videos
- speech_recognition: For speech-to-text conversion
- transformers: For text summarization
- moviepy: For audio extraction

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
