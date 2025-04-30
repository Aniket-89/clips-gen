import whisper
import json
from moviepy import *
from youtube_transcript_api import YouTubeTranscriptApi

vid = VideoFileClip("clips/short_1.mp4")

vid.audio.write_audiofile("output.mp3")

model = whisper.load_model("base")
# result = model.transcribe("output.mp3")
video_id = "3Xr7l0F9X-4"  # Only the ID, not full URL
result = YouTubeTranscriptApi.get_transcript(video_id)

t_path = "tra.json"
with open(t_path, 'w') as f:
    json.dump(result, f, indent=2)
    
print(result["text"])