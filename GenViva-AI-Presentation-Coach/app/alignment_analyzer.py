import re
from typing import Dict, Any

def calculate_alignment(slide_text: str, transcript: str) -> Dict[str, Any]:
    """
    Calculates a simple word-overlap alignment score between slide text and transcript.
    """
    def get_words(text: str) -> set:
        # Remove slide markers and transcript headers
        clean = re.sub(r'\[SLIDE \d+:[^\]]*\]|\[TRANSCRIPT SECTION \d+\]', '', text)
        # Extract individual words
        words = re.findall(r"\b[a-zA-Z']+\b", clean.lower())
        
        # Stopwords to filter out for a more meaningful overlap
        stopwords = {
            "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", 
            "to", "of", "in", "on", "for", "with", "this", "that", "it", "by", "as"
        }
        return {word for word in words if word not in stopwords}

    slide_words = get_words(slide_text)
    transcript_words = get_words(transcript)
    
    if not slide_words:
        score = 0.0
        overlap = []
    else:
        intersection = slide_words.intersection(transcript_words)
        score = len(intersection) / len(slide_words)
        overlap = sorted(list(intersection))
        
    return {
        "alignment_score": round(score, 2),
        "unique_slide_words_count": len(slide_words),
        "unique_transcript_words_count": len(transcript_words),
        "overlap_words": overlap
    }

if __name__ == "__main__":
    sample_slide = "[SLIDE 1] - presentation anxiety affects 75% of students\n- standard feedback is generic"
    sample_trans = "[TRANSCRIPT SECTION 1] Today we talk about anxiety in students and how standard feedback is generic."
    print(calculate_alignment(sample_slide, sample_trans))

