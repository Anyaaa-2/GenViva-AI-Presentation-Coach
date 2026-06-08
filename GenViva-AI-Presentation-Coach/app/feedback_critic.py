from typing import Dict, Any, List

def critique_feedback(
    feedback_result: Dict[str, Any],
    slide_wise_alignment: List[Dict[str, Any]],
    speech_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluates the generated feedback quality using rule-based metrics
    for specificity, actionability, and evidence grounding.
    """
    warnings = []
    
    # 1. Evidence Grounding Score Evaluation
    # Find all slides with Weak alignment in the actual results
    weak_slides_in_data = [slide["slide_number"] for slide in slide_wise_alignment if slide.get("alignment_label") == "Weak"]
    
    feedback_text = (feedback_result.get("alignment_feedback", "") + " " + 
                     " ".join(feedback_result.get("priority_improvements", []))).lower()
    
    grounding_score = 1.0
    if weak_slides_in_data:
        mentioned_slides = []
        for slide_num in weak_slides_in_data:
            if str(slide_num) in feedback_text:
                mentioned_slides.append(slide_num)
        
        if not mentioned_slides:
            grounding_score = 0.4
            warnings.append("Weak slide-speech alignment detected in data but slide numbers are not referenced in alignment feedback.")
        elif len(mentioned_slides) < len(weak_slides_in_data):
            grounding_score = 0.7
            warnings.append("Some weak slides were identified in data but not all were referenced in alignment feedback.")
    
    # 2. Actionability Score Evaluation
    priority_count = len(feedback_result.get("priority_improvements", []))
    if priority_count == 0:
        actionability_score = 0.2
        warnings.append("No priority improvements provided in feedback, reducing actionability.")
    elif priority_count <= 2:
        actionability_score = 0.8
    else:
        actionability_score = 1.0

    # 3. Specificity Score Evaluation
    delivery_text = feedback_result.get("delivery_feedback", "").lower()
    mentions_slides = any(char.isdigit() for char in feedback_text)
    mentions_fillers = any(word in delivery_text for word in ["filler", "um", "uh", "like", "basically", "actually"])
    
    if mentions_slides and mentions_fillers:
        specificity_score = 1.0
    elif mentions_slides or mentions_fillers:
        specificity_score = 0.6
    else:
        specificity_score = 0.2
        warnings.append("Feedback is generic; try to reference specific slide numbers or exact filler words.")

    # 4. Content Consistency Warnings
    filler_count = speech_result.get("filler_words_count", 0)
    if filler_count > 5:
        if not any(word in delivery_text for word in ["filler", "um", "uh", "like", "basically", "actually"]):
            warnings.append("High filler word count detected but delivery feedback does not address them.")
            
    alignment_text = feedback_result.get("alignment_feedback", "").lower()
    if weak_slides_in_data and not alignment_text:
        warnings.append("Slide alignment is weak but alignment feedback section is empty.")

    # 5. Critic Summary
    summary_parts = []
    avg_score = (grounding_score + actionability_score + specificity_score) / 3.0
    if avg_score >= 0.8:
        summary_parts.append("The generated feedback is of high quality, actionable, and well-grounded in presentation evidence.")
    elif avg_score >= 0.5:
        summary_parts.append("The generated feedback is moderate quality but has gaps in details or actionability.")
    else:
        summary_parts.append("The generated feedback is poor quality and requires adjustments.")
        
    if warnings:
        summary_parts.append(f"Critic flagged {len(warnings)} issue(s) that should be addressed to improve coaching quality.")
    else:
        summary_parts.append("No issues or inconsistencies were flagged by the critic.")
        
    critic_summary = " ".join(summary_parts)

    return {
        "critic_summary": critic_summary,
        "feedback_specificity_score": round(specificity_score, 2),
        "feedback_actionability_score": round(actionability_score, 2),
        "evidence_grounding_score": round(grounding_score, 2),
        "warnings": warnings
    }

if __name__ == "__main__":
    # Test block
    mock_feedback = {
        "overall_summary": "Pacing is good but structure can be improved.",
        "delivery_feedback": "Keep up the good pacing.",
        "alignment_feedback": "",
        "priority_improvements": []
    }
    mock_slides = [
        {"slide_number": 1, "alignment_score": 0.20, "alignment_label": "Weak"}
    ]
    mock_speech = {
        "total_words": 100,
        "filler_words_count": 8,
        "pace_label": "Good pace"
    }
    
    critique = critique_feedback(mock_feedback, mock_slides, mock_speech)
    import pprint
    pprint.pprint(critique)
