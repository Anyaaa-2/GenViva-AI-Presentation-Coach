import re
from typing import Dict, Any

def analyze_slides(slide_text: str) -> Dict[str, Any]:
    """
    Splits slide text into individual slides and returns the count and list of slides.
    Each slide is identified by the [SLIDE X: Title] marker.
    """
    # Use lookahead to split by slide markers, keeping the markers with the text
    parts = re.split(r'(?=\[SLIDE \d+)', slide_text)
    
    # Filter out empty sections and strip whitespace
    slides = [p.strip() for p in parts if p.strip()]
    
    return {
        "num_slides": len(slides),
        "slides": slides
    }

if __name__ == "__main__":
    sample_text = """
    [SLIDE 1: Title]
    PitchPilot presentation
    - An AI coach for students
    [SLIDE 2: Problem Statement]
    - Presentation anxiety affects 75% of students
    - Standard feedback is generic
    """
    print(analyze_slides(sample_text))

