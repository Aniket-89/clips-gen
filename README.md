# 🎬 AutoShorts Generator

An AI-powered tool to **automatically generate viral YouTube Shorts** from long-form videos.

🚀 Save hours of manual editing. Just input a YouTube link — and get punchy, vertical clips ready to go.

---

## ✨ Features

- 🎥 Download YouTube videos using `yt-dlp`
- 🔊 Transcribe audio using OpenAI Whisper or YouTube transcripts
- 🧠 Detect engaging highlights using impact words, silence, and emotional cues
- 📱 Convert clips to vertical 9:16 format (1080x1920)
- 🔤 Add MrBeast-style captions
- 🧩 Output multiple Shorts from one video

---

## 🔧 Requirements

- Python 3.10+
- `ffmpeg` installed on your system
- macOS / Linux compatible (Windows support coming soon)

---

## ⚙️ Installation

### 1. Install ffmpeg:
```bash
# On macOS (Homebrew)
brew install ffmpeg
```

# On Ubuntu/Debian
```bash
sudo apt install ffmpeg
```
### 2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
```
### 3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 🖥️ Usage

# Option 1: Streamlit UI (Easy)
```bash
streamlit run app.py
```

# Option 2: CLI (More control)
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

# Optional:
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --max-clips 5
```

### 📂 Output Structure

The tool creates the following directories:
```bash
input/         # Downloaded YouTube videos
audio/         # Extracted audio tracks
transcripts/   # Generated transcripts
clips/         # Raw highlight segments
output/        # Final Shorts with captions
```

### 🧠 How It Works

1. Downloads the video using yt-dlp
2. Gets transcript using YouTube API or Whisper
3. Analyzes for impactful segments using:
    -Trigger words (e.g. "unbelievable", "million", "crazy")
    -Emotion detection
    -Silence & natural speech boundaries
4. Extracts and crops to 9:16 format
5. Adds subtitles
6. Saves each short as a separate file (max 60s)

### 🛠️ Highlight Detection Logic

✅ Trigger words: emotional or high-impact language
✅ Short/long sentences that signal turning points
✅ Emotion-based tone shifts
✅ Start/end cues based on silence or paragraph structure
(This logic is improving — contributions welcome!)

## 📌 Notes

Output Shorts are max 60s
Subtitles have white text + black stroke
Demo video samples coming soon


## 🧑‍💻 Contribute

Want to improve clip scoring, add better captions, or support TikTok?
Contributions, ideas & PRs are welcome!

## 📣 Credits

yt-dlp for video downloads
OpenAI Whisper for transcription
Built with ❤️ using Python, MoviePy, Streamlit, and more

## 🌐 License

MIT License. Use freely, even commercially — just give credit.

## 🚀 Start Creating!

Ready to turn your long-form video into viral clips?
Fork this repo, add your own style, and build on top.


---

Let me know if you'd like:
- A GitHub Release Note or GitHub repo description  
- A tweet or LinkedIn post copy  
- A small “demo.gif” for the repo showcase  

Post it now, this looks solid for MVP open source drop 🔥