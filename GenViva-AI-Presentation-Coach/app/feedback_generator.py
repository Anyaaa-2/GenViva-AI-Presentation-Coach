from typing import Dict, Any, List

def generate_feedback(
    speech_result: Dict[str, Any],
    overall_alignment_result: Dict[str, Any],
    slide_wise_alignment: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generates structured, actionable presentation feedback using rule-based checks.
    """
    delivery_feedback = []
    alignment_feedback = []
    priority_improvements = []
    
    # 1. Delivery / Pacing Feedback
    pace_label = speech_result.get("pace_label")
    if pace_label == "Too fast":
        delivery_feedback.append("Your pacing is too fast. Try to slow down, pause between sections, and give the audience time to absorb the information.")
        priority_improvements.append("Slow down your speech pacing to keep it under 160 WPM.")
    elif pace_label == "Too slow":
        delivery_feedback.append("Your pacing is a bit slow. Try speaking slightly faster to maintain audience engagement.")
        priority_improvements.append("Increase speech pacing slightly to be above 110 WPM.")
    else:
        delivery_feedback.append("Your delivery pacing is at a good speed.")
        
    # 2. Delivery / Filler Words Feedback
    filler_count = speech_result.get("filler_words_count", 0)
    filler_rate = speech_result.get("filler_words_per_minute", 0.0) or 0.0
    if filler_count > 10 or filler_rate > 5.0:
        delivery_feedback.append(f"You used {filler_count} filler words. Try to reduce filler words by pausing silently instead of using fillers.")
        priority_improvements.append("Reduce the usage of filler words by practicing transitions and comfortable pauses.")
    else:
        delivery_feedback.append("Great job keeping filler words minimal!")
        
    # 3. Overall Alignment Feedback
    overall_score = overall_alignment_result.get("alignment_score", 0.0)
    if overall_score < 0.50:
        alignment_feedback.append("Your speech has low overall alignment with your slides. Suggest explaining slide content more clearly and mentioning core terms listed on your slides.")
        priority_improvements.append("Improve overall slide-speech alignment by speaking directly to the slide bullet points.")
    elif overall_score < 0.75:
        alignment_feedback.append("Your speech matches the slide topics reasonably well, but you could touch upon a few more key points.")
    else:
        alignment_feedback.append("Excellent alignment between slides and speech!")
        
    # 4. Slide-wise Weak Alignment Feedback
    weak_slides = []
    for slide in slide_wise_alignment:
        if slide.get("alignment_label") == "Weak":
            weak_slides.append(slide.get("slide_number"))
            
    if weak_slides:
        alignment_feedback.append(f"Slides with Weak alignment: {', '.join(map(str, weak_slides))}.")
        priority_improvements.append(f"Revise and rehearse speech sections for weak slides: {', '.join(map(str, weak_slides))}.")
        
    # 5. Overall Summary
    summary_parts = []
    if overall_score >= 0.70:
        summary_parts.append("The presentation is highly structured and matches slide contents well.")
    else:
        summary_parts.append("The presentation structure needs minor adjustments to synchronize speech with slides.")
        
    if filler_count > 10 or pace_label in ["Too fast", "Too slow"]:
        summary_parts.append("Pacing and speech delivery could be improved for better clarity and impact.")
    else:
        summary_parts.append("Delivery and pacing are strong.")
        
    overall_summary = " ".join(summary_parts)
    
    return {
        "overall_summary": overall_summary,
        "delivery_feedback": "\n".join(delivery_feedback),
        "alignment_feedback": "\n".join(alignment_feedback),
        "priority_improvements": priority_improvements
    }

if __name__ == "__main__":
    # Small test harness
    mock_speech = {
        "total_words": 150,
        "filler_words_count": 12,
        "filler_distribution": {"um": 8, "like": 4},
        "words_per_minute": 150.0,
        "filler_words_per_minute": 6.0,
        "pace_label": "Good pace"
    }
    mock_overall_alignment = {
        "alignment_score": 0.45,
        "overlap_words": ["ai", "feedback"]
    }
    mock_slide_alignment = [
        {"slide_number": 1, "alignment_score": 0.80, "alignment_label": "Strong"},
        {"slide_number": 2, "alignment_score": 0.30, "alignment_label": "Weak"}
    ]
    
    feedback = generate_feedback(mock_speech, mock_overall_alignment, mock_slide_alignment)
    import pprint
    pprint.pprint(feedback)
