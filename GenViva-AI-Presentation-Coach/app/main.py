import os
from slide_analyzer import analyze_slides
from speech_analyzer import analyze_speech
from alignment_analyzer import calculate_alignment, calculate_slide_wise_alignment
from feedback_generator import generate_feedback
from feedback_critic import critique_feedback

def run_starter_pipeline():
    """
    Main entry point for the PitchPilot starter version.
    Reads sample files, performs basic analysis, and prints findings.
    """
    # Determine base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    slide_file = os.path.join(base_dir, "data", "sample_inputs", "sample_slide_text.txt")
    transcript_file = os.path.join(base_dir, "data", "sample_inputs", "sample_transcript.txt")
    
    # Check if files exist
    if not os.path.exists(slide_file) or not os.path.exists(transcript_file):
        print(f"Error: Sample files not found.\nExpected slide path: {slide_file}\nExpected transcript path: {transcript_file}")
        return
        
    # Read files
    with open(slide_file, "r") as f:
        slide_text = f.read()
    with open(transcript_file, "r") as f:
        transcript_text = f.read()
        
    print("=" * 60)
    print("           PITCHPILOT: AI PRESENTATION COACH (STARTER)      ")
    print("=" * 60)
    
    # 1. Slide Analysis
    slide_results = analyze_slides(slide_text)
    print(f"\n[1] Slide Analysis:")
    print(f"    - Total Slides Found: {slide_results['num_slides']}")
    print(f"    - Slides List Preview:")
    for idx, slide in enumerate(slide_results['slides']):
        # Get first line of slide content as header
        header = slide.split('\n')[0]
        print(f"      * Slide {idx+1}: {header}")
        
    # 2. Speech Analysis (v0.2: passing duration_minutes=2.0)
    sample_duration = 2.0
    speech_results = analyze_speech(transcript_text, duration_minutes=sample_duration)
    print(f"\n[2] Speech & Delivery Analysis:")
    print(f"    - Total Word Count: {speech_results['total_words']}")
    print(f"    - Filler Word Count: {speech_results['filler_words_count']}")
    if speech_results['words_per_minute'] is not None:
        print(f"    - Presentation Duration: {sample_duration} minutes")
        print(f"    - Pacing: {speech_results['words_per_minute']} WPM ({speech_results['pace_label']})")
        print(f"    - Filler Pacing Rate: {speech_results['filler_words_per_minute']} fillers/min")
    print(f"    - Filler Word Distribution:")
    for filler, count in speech_results['filler_distribution'].items():
        print(f"      * '{filler}': {count}")
        
    # 3. Alignment Analysis
    alignment_results = calculate_alignment(slide_text, transcript_text)
    slide_alignment_results = calculate_slide_wise_alignment(slide_results['slides'], transcript_text)
    
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
            
    # 4. Coaching Feedback Generator (v0.5)
    coaching_results = generate_feedback(speech_results, alignment_results, slide_alignment_results)
    
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
        
    # 5. Feedback Critic (v0.6)
    critic_results = critique_feedback(coaching_results, slide_alignment_results, speech_results)
    
    print(f"\n[5] PitchPilot Feedback Critic Evaluator:")
    print(f"    - Quality Metrics:")
    print(f"      * Specificity Score: {critic_results['feedback_specificity_score']:.2f}")
    print(f"      * Actionability Score: {critic_results['feedback_actionability_score']:.2f}")
    print(f"      * Evidence Grounding Score: {critic_results['evidence_grounding_score']:.2f}")
    print(f"    - Critic Summary: {critic_results['critic_summary']}")
    
    if critic_results['warnings']:
        print(f"    - Warnings:")
        for idx, warn in enumerate(critic_results['warnings']):
            print(f"      * Warning {idx+1}: {warn}")
    else:
        print(f"    - Warnings: None")
    
    print("\n" + "=" * 60)
    print("                      ANALYSIS COMPLETE                     ")
    print("=" * 60)

if __name__ == "__main__":
    run_starter_pipeline()

