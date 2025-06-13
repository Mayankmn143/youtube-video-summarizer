#!/usr/bin/env python3
"""
YouTube Video Summarizer
A tool to download YouTube videos, extract audio, and generate summaries.
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path

try:
    import yt_dlp
    import speech_recognition as sr
    from moviepy.editor import VideoFileClip
    from transformers import pipeline
    import warnings
    warnings.filterwarnings("ignore")
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)


class YouTubeSummarizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.summarizer = None
        
    def download_video(self, url, output_path):
        """Download YouTube video using yt-dlp"""
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')
                video_file = output_path / f"{video_title}.mp4"
                return video_file, video_title
                
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None, None
    
    def extract_audio(self, video_file, audio_file):
        """Extract audio from video file"""
        try:
            video = VideoFileClip(str(video_file))
            audio = video.audio
            audio.write_audiofile(str(audio_file), verbose=False, logger=None)
            audio.close()
            video.close()
            return True
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return False
    
    def transcribe_audio(self, audio_file):
        """Convert audio to text using speech recognition"""
        try:
            with sr.AudioFile(str(audio_file)) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def summarize_text(self, text):
        """Generate summary using transformers"""
        try:
            if self.summarizer is None:
                self.summarizer = pipeline("summarization", 
                                          model="facebook/bart-large-cnn")
            
            # Split text into chunks if too long
            max_chunk = 1024
            chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
            
            summaries = []
            for chunk in chunks:
                if len(chunk.strip()) > 50:  # Only summarize substantial chunks
                    summary = self.summarizer(chunk, 
                                            max_length=150, 
                                            min_length=30, 
                                            do_sample=False)
                    summaries.append(summary[0]['summary_text'])
            
            return ' '.join(summaries)
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
    
    def process_video(self, url):
        """Main processing function"""
        print(f"Processing video: {url}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Download video
            print("Downloading video...")
            video_file, title = self.download_video(url, temp_path)
            if not video_file:
                return None
            
            # Extract audio
            print("Extracting audio...")
            audio_file = temp_path / "audio.wav"
            if not self.extract_audio(video_file, audio_file):
                return None
            
            # Transcribe audio
            print("Transcribing audio...")
            text = self.transcribe_audio(audio_file)
            if not text:
                return None
            
            # Generate summary
            print("Generating summary...")
            summary = self.summarize_text(text)
            
            return {
                'title': title,
                'transcription': text,
                'summary': summary
            }


def main():
    parser = argparse.ArgumentParser(description='YouTube Video Summarizer')
    parser.add_argument('--url', required=True, help='YouTube video URL')
    parser.add_argument('--output', help='Output file for results')
    
    args = parser.parse_args()
    
    summarizer = YouTubeSummarizer()
    result = summarizer.process_video(args.url)
    
    if result:
        print(f"\n{'='*50}")
        print(f"Video: {result['title']}")
        print(f"{'='*50}")
        print(f"\nSummary:")
        print(result['summary'])
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Title: {result['title']}\n\n")
                f.write(f"Summary:\n{result['summary']}\n\n")
                f.write(f"Full Transcription:\n{result['transcription']}")
            print(f"\nResults saved to: {args.output}")
    else:
        print("Failed to process video")


if __name__ == "__main__":
    main()
