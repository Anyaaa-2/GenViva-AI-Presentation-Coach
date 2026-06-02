import re
from typing import Dict, Any

def get_words(text: str) -> set:
    """
    Cleans slide or transcript text and extracts a set of unique words,
    filtering out common stopwords and formatting headers/markers.
    """
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

def get_alignment_feedback(score: float) -> tuple:
    """
    Returns an alignment label ("Strong", "Moderate", "Weak") and a short,
    actionable feedback message based on the alignment score.
    """
    if score >= 0.70:
        return "Strong", "Excellent alignment! Your speech closely matches the bullet points on this slide."
    elif score >= 0.40:
        return "Moderate", "Good overlap, but consider referencing more of the slide's key points in your speech."
    else:
        return "Weak", "Low alignment. Try to explicitly discuss the keywords listed on this slide to guide the audience."

def calculate_alignment(slide_text: str, transcript: str) -> Dict[str, Any]:
    """
    Calculates a simple word-overlap alignment score between slide text and transcript.
    """
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

def calculate_slide_wise_alignment(slides: list, transcript: str) -> list:
    """
    Compares each slide in the slides list with the overall transcript using a cleaned word-overlap logic.
    Returns a list of dictionaries with slide alignment metrics and feedback.
    """
    results = []
    transcript_words = get_words(transcript)
    
    for idx, slide_text in enumerate(slides):
        # Extract slide number from marker like '[SLIDE 1: Title]', falling back to index + 1
        match = re.search(r'\[SLIDE\s+(\d+)', slide_text)
        slide_number = int(match.group(1)) if match else (idx + 1)
        
        slide_words = get_words(slide_text)
        
        if not slide_words:
            score = 0.0
            overlap = []
        else:
            intersection = slide_words.intersection(transcript_words)
            score = len(intersection) / len(slide_words)
            overlap = sorted(list(intersection))
            
        label, message = get_alignment_feedback(score)
        
        results.append({
            "slide_number": slide_number,
            "alignment_score": round(score, 2),
            "alignment_label": label,
            "feedback_message": message,
            "shared_words_count": len(overlap),
            "shared_words_sample": overlap
        })
        
    return results

if __name__ == "__main__":
    sample_slide = "[SLIDE 1] - presentation anxiety affects 75% of students\n- standard feedback is generic"
    sample_trans = "[TRANSCRIPT SECTION 1] Today we talk about anxiety in students and how standard feedback is generic."
    print("Overall Alignment:")
    print(calculate_alignment(sample_slide, sample_trans))
    
    print("\nSlide-wise Alignment:")
    sample_slides = [
        "[SLIDE 1: Title] Today we introduce PitchPilot",
        "[SLIDE 2: Problem] presentation anxiety affects 75% of students and standard feedback is generic"
    ]
    print(calculate_slide_wise_alignment(sample_slides, sample_trans))



