import os
import yt_dlp
import ffmpeg
from moviepy import *
# from moviepy.video.fx.


class VideoProcessor:
    def __init__(self, input_dir="input", audio_dir="audio"):
        self.input_dir = input_dir
        self.audio_dir = audio_dir
        
    def download_video(self, url):
        """Download YouTube video using yt-dlp"""
        output_path = os.path.join(self.input_dir, "%(title)s.%(ext)s")
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': output_path,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            return video_path
    
    def extract_audio(self, video_path):
        """Extract audio from video file"""
        filename = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(self.audio_dir, f"{filename}.wav")
        
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ac=1, ar='16k')
        ffmpeg.run(stream, overwrite_output=True)
        
        return audio_path
    
    def create_vertical_clip(self, video_path, start_time, end_time, output_path):
        """Create a vertical format clip from the original video"""
        with VideoFileClip(video_path) as clip:
            # Extract the segment
            segment = clip.subclipped(start_time, end_time)
            
            # Get original dimensions
            w, h = segment.size
            
            # Calculate new dimensions for 9:16 aspect ratio
            if (h/w) < (16/9):
                new_w = int(h * 9/16)
                # Crop from center
                x1 = int((w - new_w)/2)
                cropped = segment.cropped(x1=x1, width=new_w)
            else:
                new_h = int(w * 16/9)
                y1 = int((h - new_h)/2)
                cropped = segment.cropped(y1=y1, height=new_h)
            
            # Resize to standard short size (1080x1920)
            final_clip = cropped.resized((1080, 1920))
            # final_clip = segment
            # Write the file
            final_clip.write_videofile(output_path, 
                                     codec='libx264', 
                                     audio_codec='aac',
                                     preset='medium')