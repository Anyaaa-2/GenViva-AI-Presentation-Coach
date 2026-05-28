from typing import Dict, Any, List

def critique_feedback(
    slide_analysis: Dict[str, Any], 
    speech_analysis: Dict[str, Any], 
    alignment_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Consolidates reviews from Slide, Speech, and Alignment agents. Resolves conflicts,
    removes redundant feedback, and designs a human-centric action plan.
    
    Args:
        slide_analysis (Dict[str, Any]): Outputs from slide_analyzer.py
        speech_analysis (Dict[str, Any]): Outputs from speech_analyzer.py
        alignment_analysis (Dict[str, Any]): Outputs from alignment_analyzer.py
        
    Returns:
        Dict[str, Any]: Consolidated critic dashboard.
    """
    consolidated_suggestions = []
    conflict_logs = []
    
    # 1. Gather all recommendations
    slide_suggs = []
    for s in slide_analysis.get("slides_analysis", []):
        for suggestion in s.get("suggestions", []):
            slide_suggs.append((s["slide_number"], suggestion))
            
    speech_suggs = speech_analysis.get("suggestions", [])
    align_suggs = [a.get("suggested_fix") for a in alignment_analysis.get("alignment_report", []) if a.get("suggested_fix") != "No changes needed."]
    
    # 2. Check for typical conflicts
    # Example conflict: Slide analyzer says slide is too dense (reduce content),
    # but alignment analyzer complains that slide text wasn't spoken enough (add more speech/details).
    is_slide_dense_anywhere = any(s.get("is_dense", False) for s in slide_analysis.get("slides_analysis", []))
    is_alignment_poor_anywhere = alignment_analysis.get("average_alignment_score", 1.0) < 0.6
    
    if is_slide_dense_anywhere and is_alignment_poor_anywhere:
        conflict_logs.append("Resolved conflict: Slide is overloaded, but alignment is low. Instructed presenter to simplify slides first and speak naturally about the main themes instead of reading.")
        # Inject balanced guidance
        consolidated_suggestions.append(
            "CRITICAL: Do not try to read complex text. Simplify slide contents and practice focusing verbally only on the core message."
        )
        
    # 3. Compile clean actionable items
    for slide_num, suggestion in slide_suggs:
        if "density" in suggestion.lower() or "too long" in suggestion.lower():
            consolidated_suggestions.append(f"[Slide {slide_num}] Layout: {suggestion}")
            
    for sugg in speech_suggs:
        if "filler" in sugg.lower() or "pace" in sugg.lower():
            consolidated_suggestions.append(f"[Delivery]: {sugg}")
            
    for sugg in align_suggs:
        consolidated_suggestions.append(f"[Content Alignment]: {sugg}")
        
    # Deduplicate suggestions
    consolidated_suggestions = list(set(consolidated_suggestions))
    
    # Simple overall score formula (0-100 scale)
    avg_align = alignment_analysis.get("average_alignment_score", 1.0)
    total_fillers = speech_analysis.get("total_filler_words", 0)
    dense_slides_count = sum(1 for s in slide_analysis.get("slides_analysis", []) if s.get("is_dense", False))
    total_slides = slide_analysis.get("total_slides", 1)
    
    # Calculate performance score
    alignment_component = avg_align * 40
    filler_component = max(0, 30 - (total_fillers * 2))
    layout_component = ((total_slides - dense_slides_count) / max(total_slides, 1)) * 30
    
    overall_performance_score = round(alignment_component + filler_component + layout_component, 1)
    overall_performance_score = min(max(overall_performance_score, 0), 100) # Clamp
    
    return {
        "status": "success",
        "overall_score": overall_performance_score,
        "resolved_conflicts": conflict_logs,
        "actionable_feedback": consolidated_suggestions,
        "summary": (
            f"Your presentation scored {overall_performance_score}/100. "
            f"Focus on speaking clearly with fewer verbal pauses, and make sure your slides visual cues match your talking points."
        )
    }

if __name__ == "__main__":
    s_an = {"total_slides": 2, "slides_analysis": [{"slide_number": 1, "is_dense": True, "suggestions": ["too long"]}]}
    sp_an = {"total_filler_words": 12, "suggestions": ["High filler word frequency."]}
    al_an = {"average_alignment_score": 0.4, "alignment_report": [{"suggested_fix": "Make sure to explicitly mention: problem"}]}
    print(critique_feedback(s_an, sp_an, al_an))
