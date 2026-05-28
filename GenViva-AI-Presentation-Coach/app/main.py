import os
from slide_analyzer import analyze_slides
from speech_analyzer import analyze_speech
from alignment_analyzer import calculate_alignment

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
        
    # 2. Speech Analysis
    speech_results = analyze_speech(transcript_text)
    print(f"\n[2] Speech & Delivery Analysis:")
    print(f"    - Total Word Count: {speech_results['total_words']}")
    print(f"    - Filler Word Count: {speech_results['filler_words_count']}")
    print(f"    - Filler Word Distribution:")
    for filler, count in speech_results['filler_distribution'].items():
        print(f"      * '{filler}': {count}")
        
    # 3. Alignment Analysis
    alignment_results = calculate_alignment(slide_text, transcript_text)
    print(f"\n[3] Slide-Speech Alignment:")
    print(f"    - Alignment Score (Word Overlap): {alignment_results['alignment_score']:.2f}")
    print(f"    - Shared Content Words Count: {len(alignment_results['overlap_words'])}")
    print(f"    - Shared Words (Sample): {', '.join(alignment_results['overlap_words'][:10])}...")
    
    print("\n" + "=" * 60)
    print("                      ANALYSIS COMPLETE                     ")
    print("=" * 60)

if __name__ == "__main__":
    run_starter_pipeline()
