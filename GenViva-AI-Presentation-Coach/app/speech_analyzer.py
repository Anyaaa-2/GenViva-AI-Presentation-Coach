import re
from typing import Dict, Any

def analyze_speech(transcript: str, duration_minutes: float = None) -> Dict[str, Any]:
    """
    Calculates total word count and counts filler words in the transcript.
    If duration_minutes is provided, calculates pacing metrics (WPM and fillers/min) and pacing feedback.
    """
    # Define common filler words/phrases
    filler_words = ["um", "uh", "like", "basically", "actually", "so", "you know"]
    
    # Clean transcript text (remove section tags)
    clean_text = re.sub(r'\[TRANSCRIPT SECTION \d+\]', '', transcript)
    
    # Find all words (alphabetic sequence, case-insensitive)
    words = re.findall(r"\b[a-zA-Z']+\b", clean_text.lower())
    total_words = len(words)
    
    # Count occurrences of each filler
    filler_counts = {}
    total_fillers = 0
    text_lower = clean_text.lower()
    
    for filler in filler_words:
        # Regex word boundary check
        pattern = rf"\b{re.escape(filler)}\b"
        count = len(re.findall(pattern, text_lower))
        if count > 0:
            filler_counts[filler] = count
            total_fillers += count
            
    # Calculate pacing metrics if duration is provided
    words_per_minute = None
    filler_words_per_minute = None
    pace_label = None
    
    if duration_minutes is not None and duration_minutes > 0:
        words_per_minute = round(total_words / duration_minutes, 2)
        filler_words_per_minute = round(total_fillers / duration_minutes, 2)
        
        if words_per_minute < 110:
            pace_label = "Too slow"
        elif words_per_minute <= 160:
            pace_label = "Good pace"
        else:
            pace_label = "Too fast"
            
    return {
        "total_words": total_words,
        "filler_words_count": total_fillers,
        "filler_distribution": filler_counts,
        "words_per_minute": words_per_minute,
        "filler_words_per_minute": filler_words_per_minute,
        "pace_label": pace_label
    }

if __name__ == "__main__":
    sample_transcript = """
    [TRANSCRIPT SECTION 1]
    Hello everyone, um, welcome to my presentation. Today, I'm going to introduce, uh, PitchPilot.
    So basically, this is, like, really cool.
    """
    print("Without duration:")
    print(analyze_speech(sample_transcript))
    print("\nWith duration of 0.5 minutes:")
    print(analyze_speech(sample_transcript, duration_minutes=0.5))

