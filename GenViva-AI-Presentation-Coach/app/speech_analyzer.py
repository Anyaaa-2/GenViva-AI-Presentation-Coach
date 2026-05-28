import re
from typing import Dict, Any

def analyze_speech(transcript: str) -> Dict[str, Any]:
    """
    Calculates total word count and counts filler words in the transcript.
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
            
    return {
        "total_words": total_words,
        "filler_words_count": total_fillers,
        "filler_distribution": filler_counts
    }

if __name__ == "__main__":
    sample_transcript = """
    [TRANSCRIPT SECTION 1]
    Hello everyone, um, welcome to my presentation. Today, I'm going to introduce, uh, PitchPilot.
    So basically, this is, like, really cool.
    """
    print(analyze_speech(sample_transcript))

