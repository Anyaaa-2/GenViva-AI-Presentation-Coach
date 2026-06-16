import re
from typing import Dict, Any, List

def generate_viva_questions(
    slide_results: Dict[str, Any],
    slide_wise_alignment: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generates a list of tailored viva/QA questions based on slide text headers
    and the corresponding slide alignment scores.
    """
    questions = []
    slides = slide_results.get("slides", [])
    
    # Create a lookup for slide titles and text by slide number
    slide_lookup = {}
    for idx, slide_text in enumerate(slides):
        # Extract title from '[SLIDE X: Title]'
        match = re.search(r'\[SLIDE\s+(\d+):\s*([^\]]+)\]', slide_text)
        if match:
            slide_num = int(match.group(1))
            title = match.group(2).strip()
        else:
            slide_num = idx + 1
            title = f"Slide {slide_num}"
        slide_lookup[slide_num] = title

    for alignment in slide_wise_alignment:
        slide_num = alignment["slide_number"]
        title = slide_lookup.get(slide_num, f"Slide {slide_num}")
        label = alignment.get("alignment_label", "Moderate")
        
        if label == "Weak":
            question = f"On Slide {slide_num} ({title}), your spoken delivery did not fully cover the listed points. Can you explain the main idea of this slide in your own words?"
            reason = f"Alignment is Weak ({alignment['alignment_score']}), suggesting the speech strayed from the slide bullet points."
            difficulty = "Advanced"
        elif label == "Moderate":
            question = f"For Slide {slide_num} ({title}), why is the method, problem, or choice discussed here important for your overall presentation?"
            reason = f"Alignment is Moderate ({alignment['alignment_score']}), meaning the core topics were mentioned but could be elaborated."
            difficulty = "Intermediate"
        else:  # Strong
            question = f"You explained Slide {slide_num} ({title}) very well. How would you justify the design choices or conclusions mentioned here?"
            reason = f"Alignment is Strong ({alignment['alignment_score']}), showing good coverage of the slide content in speech."
            difficulty = "Basic"
            
        questions.append({
            "slide_number": slide_num,
            "question": question,
            "reason": reason,
            "difficulty": difficulty
        })
        
    return questions

if __name__ == "__main__":
    # Test block
    mock_slides = {
        "num_slides": 2,
        "slides": [
            "[SLIDE 1: Introduction] Introduction to PitchPilot",
            "[SLIDE 2: Tech Stack] Streamlit, FastAPI, and FAISS"
        ]
    }
    mock_alignment = [
        {
            "slide_number": 1,
            "alignment_score": 0.85,
            "alignment_label": "Strong",
            "feedback_message": "Excellent alignment!",
            "shared_words_count": 5,
            "shared_words_sample": ["pitchpilot"]
        },
        {
            "slide_number": 2,
            "alignment_score": 0.25,
            "alignment_label": "Weak",
            "feedback_message": "Low alignment.",
            "shared_words_count": 1,
            "shared_words_sample": ["streamlit"]
        }
    ]
    
    qs = generate_viva_questions(mock_slides, mock_alignment)
    import pprint
    pprint.pprint(qs)
