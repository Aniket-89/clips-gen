from PIL import Image, ImageDraw, ImageFont
from moviepy import *
import os
import whisper

model = whisper.load_model('base')

class SubtitleGenerator:
    def __init__(self, font_size=80, font_color='white', stroke_color='black', stroke_width=3):
        self.font_size = font_size
        self.font_color = font_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        
    def create_caption_clip(self, text, duration, size, font_path=None):
        """Create a TextClip with stroke effect"""
        # Use Arial Bold if no font specified (you may want to include a custom font)
        if font_path is None:
            font_path = "Arial-Bold" if os.name == 'posix' else "arialbd.ttf"
            
        text_clip = TextClip(
            font='Branda-yolq.ttf',
            text=text,
            font_size=self.font_size,
            color=self.font_color,
            stroke_color=self.stroke_color,
            stroke_width=self.stroke_width,
            size=size,
            method='caption',
            # align='center'
        )
        return text_clip.with_duration(duration)
    

    def create_clip_transcript(self, video):
        video.audio.write_audiofile("audio.mp3")
        result = model.transcribe("audio.mp3")
        return result['segments']
    
    def add_captions_to_video(self, video_path, transcript, output_path):
        """Add captions to video clip"""
        with VideoFileClip(video_path) as video:
            # Video dimensions
            W, H = video.size
            transcript = self.create_clip_transcript(video)
            # Create text clips for each segment
            text_clips = []
            
            
            for segment in transcript:
                start_time = segment['start']
                duration = segment['end'] - segment['start']  # Default 3s if not specified
                print('id: ' + str(segment['id']) + ", duration: " + str(duration) )
                text = segment['text']
                
                txt_clip = self.create_caption_clip(
                    text,
                    duration,
                    (W, None)  # Width of video, height automatic
                )
                
                # Position at the bottom with some padding
                txt_clip = txt_clip.with_position(('center', 0.8), relative=True)
                txt_clip = txt_clip.with_duration(duration)
                txt_clip = txt_clip.with_start(start_time)
                
                text_clips.append(txt_clip)
                start_time += duration
            # Combine video with all text clips
            final = CompositeVideoClip([video] + text_clips)
            
            # Write final video
            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                preset='medium'
            )