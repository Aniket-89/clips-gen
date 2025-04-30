import os
import argparse
import whisper
import json
from youtube_transcript_api import YouTubeTranscriptApi
from .video_processor import VideoProcessor
from .highlight_detector import HighlightDetector
from .subtitle_generator import SubtitleGenerator
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    parsed_url = urlparse(url)
    
    # Standard watch URLs: https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    
    # Shortened URLs: https://youtu.be/VIDEO_ID
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    
    return None

def ensure_directories():
    """Ensure all required directories exist"""
    dirs = ['input', 'audio', 'transcripts', 'clips', 'captions', 'output']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)

def process_video(url: str, max_clips: int = 3):
    """Process a YouTube video and create shorts"""
    ensure_directories()
    
    # Initialize components
    video_proc = VideoProcessor()
    highlight_detector = HighlightDetector()
    subtitle_gen = SubtitleGenerator()
    
    # Step 1: Download video
    print("Downloading video...")
    video_path = video_proc.download_video(url)

    # Step 2: Extract audio
    print("Extracting audio...")
    audio_path = video_proc.extract_audio(video_path)

    # Step 3: Transcribe audio
    print("Transcribing audio...")
    # model = whisper.load_model("base")
    # result = model.transcribe(audio_path)
    video_id = extract_video_id(url)  # Only the ID, not full URL
    result = YouTubeTranscriptApi.get_transcript(video_id)

    # Save transcript
    transcript_path = os.path.join("transcripts", f"{os.path.splitext(os.path.basename(video_path))[0]}.json")
    with open(transcript_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Step 4: Detect highlights
    print("Finding highlights...")
    highlights = highlight_detector.find_highlights(result, num_clips=max_clips)
    
    # Step 5: Create clips
    print("Creating clips...")
    generated_clips = []
    for idx, highlight in enumerate(highlights, 1):
        clip_name = f"short_{idx}.mp4"
        clip_path = os.path.join("clips", clip_name)
        
        # Create vertical clip
        video_proc.create_vertical_clip(
            video_path,
            highlight.start_time,
            highlight.end_time,
            clip_path
        )
        
        # Add captions
        output_path = os.path.join("clips", f"short_{idx}.mp4")
        # relevant_segments = [
        #     seg for seg in result["segments"]
        #     if seg["start"] >= highlight.start_time and seg["end"] <= highlight.end_time
        # ]
        
        # subtitle_gen.add_captions_to_video(clip_path, relevant_segments, output_path)
        generated_clips.append(output_path)
    
    vids = []
    print("\nGenerated shorts:")
    
    for clip in generated_clips:
        vids.append(clip)
        # print(f"- {clip}")
    return vids

def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts Generator")
    parser.add_argument("url", help="YouTube video URL to process")
    parser.add_argument("--max-clips", type=int, default=3,
                      help="Maximum number of shorts to generate (default: 3)")
    
    args = parser.parse_args()
    process_video(args.url, args.max_clips)

if __name__ == "__main__":
    main()