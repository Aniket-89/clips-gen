import json
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Highlight:
    start_time: float
    end_time: float
    text: str
    score: float

class HighlightDetector:
    def __init__(self):
        self.trigger_words = {
    'high_impact': [
        'die', 'death', 'danger', 'dangerous', 'kill', 'killed', 'crazy', 'insane',
        'unbelievable', 'shocking', 'mind-blowing', 'disaster', 'collapse'
    ],
    'value': [
        'million', 'billion', 'dollars', 'rupees', 'crore', 'lakh', 'money', 'cash',
        'profit', 'free', 'jackpot', 'deal', 'rich', 'investment'
    ],
    'emotion': [
        'love', 'hate', 'best', 'worst', 'never', 'ever', 'scared', 'afraid', 'happy', 
        'sad', 'angry', 'excited', 'terrified', 'worried', 'anxious', 'thrilled', 
        'devastated', 'emotional', 'crying', 'laughing', 'screaming', 'frightened',
        'heartbreaking', 'beautiful', 'amazing', 'hilarious'
    ],
    'emphasis': [
        'very', 'extremely', 'absolutely', 'completely', 'totally', 'literally', 
        'honestly', 'seriously', 'really', 'so', 'super', 'ultra', 'mega', '!', '!!', '!!!'
    ]
}

        
        # Emotion indicators in text
        self.emotion_markers = ['!', '...', '???', 'oh my god', 'oh my', 'wow']
        # Minimum pause duration (in seconds) to consider as significant
        self.min_pause_duration = 1.0
        
    def load_transcript(self, transcript_path: str) -> List[dict]:
        """Load and parse the whisper transcript JSON"""
        with open(transcript_path, 'r') as f:
            return json.load(f)
    
    def detect_emotion_intensity(self, text: str) -> float:
        """Detect emotional intensity in text based on various indicators"""
        intensity = 0
        text_lower = text.lower()
        
        # Check for emotion markers
        for marker in self.emotion_markers:
            if marker in text_lower:
                intensity += 1
        
        # Count exclamation marks
        intensity += text.count('!') * 0.5
        
        # Check for repeated letters (e.g., "nooooo", "wowwww")
        words = text_lower.split()
        for word in words:
            if any(letter * 3 in word for letter in 'aeiouwy'):
                intensity += 0.5
                
        # Check for ALL CAPS words
        caps_words = sum(1 for word in text.split() if word.isupper() and len(word) > 2)
        intensity += caps_words * 0.5
        
        return intensity
    
    def detect_pause_significance(self, current_segment: dict, next_segment: dict = None) -> float:
        """Calculate the significance of a pause between segments"""
        if not next_segment:
            return 0
            
        # Calculate pause duration between segments
        pause_duration = next_segment.get('start', 0) - (current_segment.get('start', 0) + current_segment.get('duration', 0))
        
        if pause_duration >= self.min_pause_duration:
            # Score longer pauses higher, but with diminishing returns
            return min(2.0, pause_duration / 2)
        return 0
    
    def score_segment(self, text: str, current_segment: dict = None, next_segment: dict = None) -> float:
        """Score a text segment based on various factors"""
        score = 0
        words = text.lower().split()
        
        # Check for trigger words with weighted categories
        for category, triggers in self.trigger_words.items():
            multiplier = {
                'high_impact': 2,
                'emotion': 2.5,  # Increased weight for emotional content
                'emphasis': 1.5,
                'value': 1
            }.get(category, 1)
            score += sum(word in triggers for word in words) * multiplier
        
        # Add emotional intensity score
        score += self.detect_emotion_intensity(text) * 2
        
        # Add pause significance if available
        if current_segment and next_segment:
            score += self.detect_pause_significance(current_segment, next_segment)
        
        # Length factor (prefer 10-30 words)
        word_count = len(words)
        if 10 <= word_count <= 30:
            score += 1
        
        # Sentence structure (prefer complete sentences)
        if text.strip().endswith(('.', '!', '?')):
            score += 0.5
        
        return score
    
    def find_highlights(self, transcript: List[dict], min_duration: float = 25, 
                       max_duration: float = 60, num_clips: int = 3) -> List[Highlight]:
        """Find the most engaging segments in the transcript"""
        highlights = []
        current_segment = {'text': [], 'start': 0, 'duration': 0}

        for segment in transcript:
            # Accumulate segments until we hit minimum duration
            current_segment['text'].append(segment['text'])
            # current_segment['duration'] += (segment['end'] - segment['start'])
            current_segment['duration'] += segment['duration']
            if current_segment['duration'] >= min_duration:
                text = ' '.join(current_segment['text'])
                score = self.score_segment(text)
                
                if current_segment['duration'] <= max_duration:
                    highlights.append(Highlight(
                        start_time=current_segment['start'],
                        end_time=current_segment['start'] + current_segment['duration'],
                        text=text,
                        score=score
                    ))
                
                # Start new segment
                current_segment = {'text': [], 'start': segment['start'], 'duration': 0}
        
        # Sort by score and return top N highlights
        highlights.sort(key=lambda x: x.score, reverse=True)
        return highlights[:num_clips]
    
    def get_highlight_timestamps(self, transcript_path: str) -> List[Tuple[float, float]]:
        """Get start and end timestamps for the best highlights"""
        transcript = self.load_transcript(transcript_path)
        highlights = self.find_highlights(transcript)
        return [(h.start_time, h.end_time) for h in highlights]