from typing import Dict, Any, List

def print_header():
    """Prints report start decorative header."""
    print("=" * 60)
    print("           PITCHPILOT: AI PRESENTATION COACH (STARTER)      ")
    print("=" * 60)

def print_slide_analysis(slide_results: Dict[str, Any]):
    """Prints slide analysis summary details."""
    print(f"\n[1] Slide Analysis:")
    print(f"    - Total Slides Found: {slide_results['num_slides']}")
    print(f"    - Slides List Preview:")
    for idx, slide in enumerate(slide_results['slides']):
        header = slide.split('\n')[0]
        print(f"      * Slide {idx+1}: {header}")

def print_speech_analysis(speech_results: Dict[str, Any], duration_minutes: float = 2.0):
    """Prints speech count, pacing, filler words analysis."""
    print(f"\n[2] Speech & Delivery Analysis:")
    print(f"    - Total Word Count: {speech_results['total_words']}")
    print(f"    - Filler Word Count: {speech_results['filler_words_count']}")
    if speech_results['words_per_minute'] is not None:
        print(f"    - Presentation Duration: {duration_minutes} minutes")
        print(f"    - Pacing: {speech_results['words_per_minute']} WPM ({speech_results['pace_label']})")
        print(f"    - Filler Pacing Rate: {speech_results['filler_words_per_minute']} fillers/min")
    print(f"    - Filler Word Distribution:")
    for filler, count in speech_results['filler_distribution'].items():
        print(f"      * '{filler}': {count}")

def print_alignment_analysis(alignment_results: Dict[str, Any], slide_alignment_results: List[Dict[str, Any]]):
    """Prints overall and slide-wise alignment scores/feedback."""
    print(f"\n[3] Slide-Speech Alignment:")
    print(f"    - Overall Alignment Score (Word Overlap): {alignment_results['alignment_score']:.2f}")
    print(f"    - Shared Content Words Count: {len(alignment_results['overlap_words'])}")
    print(f"    - Shared Words (Sample): {', '.join(alignment_results['overlap_words'][:10])}...")
    
    print(f"\n    - Slide-wise Alignment Scores & Feedback:")
    for res in slide_alignment_results:
        print(f"      * Slide {res['slide_number']}: Score = {res['alignment_score']:.2f} | Label = {res['alignment_label']}")
        print(f"        Feedback: {res['feedback_message']}")
        if res['shared_words_sample']:
            print(f"        Shared words sample: {', '.join(res['shared_words_sample'][:5])}")
        else:
            print(f"        Shared words sample: (None)")

def print_feedback_summary(coaching_results: Dict[str, Any]):
    """Prints Coaching Feedback details including delivery feedback and improvements list."""
    print(f"\n[4] PitchPilot Coaching Summary:")
    print(f"    - Overall Summary: {coaching_results['overall_summary']}")
    
    print(f"\n    - Delivery Coaching:")
    for line in coaching_results['delivery_feedback'].split('\n'):
        if line.strip():
            print(f"      * {line}")
            
    print(f"\n    - Slide Alignment Coaching:")
    for line in coaching_results['alignment_feedback'].split('\n'):
        if line.strip():
            print(f"      * {line}")
            
    print(f"\n    - Priority Improvements:")
    if coaching_results['priority_improvements']:
        for idx, imp in enumerate(coaching_results['priority_improvements']):
            print(f"      {idx+1}. {imp}")
    else:
        print("      No critical improvements needed. Excellent presentation!")

def print_critic_report(critic_results: Dict[str, Any]):
    """Prints Critic quality scores, diagnostic summary, and warning items."""
    print(f"\n[5] PitchPilot Feedback Critic Evaluator:")
    print(f"    - Quality Metrics:")
    print(f"      * Specificity Score: {critic_results['feedback_specificity_score']:.2f}")
    print(f"      * Actionability Score: {critic_results['feedback_actionability_score']:.2f}")
    print(f"      * Grounding Score: {critic_results['evidence_grounding_score']:.2f}")
    print(f"    - Critic Summary: {critic_results['critic_summary']}")
    
    if critic_results['warnings']:
        print(f"    - Warnings:")
        for idx, warn in enumerate(critic_results['warnings']):
            print(f"      * Warning {idx+1}: {warn}")
    else:
        print(f"    - Warnings: None")

def print_viva_questions(viva_questions: List[Dict[str, Any]]):
    """Prints generated simulated viva questions."""
    print(f"\n[6] Viva Questions:")
    for res in viva_questions:
        print(f"      * Slide {res['slide_number']} - {res['difficulty']} Difficulty:")
        print(f"        Question: {res['question']}")
        print(f"        Reason: {res['reason']}")

def print_footer():
    """Prints footer decorative section."""
    print("\n" + "=" * 60)
    print("                      ANALYSIS COMPLETE                     ")
    print("=" * 60)
