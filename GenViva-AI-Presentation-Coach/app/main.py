import os
from slide_analyzer import analyze_slides
from speech_analyzer import analyze_speech
from alignment_analyzer import calculate_alignment, calculate_slide_wise_alignment
from feedback_generator import generate_feedback
from feedback_critic import critique_feedback
from viva_generator import generate_viva_questions
from report_formatter import (
    print_header,
    print_slide_analysis,
    print_speech_analysis,
    print_alignment_analysis,
    print_feedback_summary,
    print_critic_report,
    print_viva_questions,
    print_footer
)

def run_starter_pipeline():
    """
    Main entry point for the PitchPilot starter version.
    Reads sample files, performs analysis, and prints formatted reports.
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
        
    # Print Header Section
    print_header()
    
    # 1. Slide Analysis
    slide_results = analyze_slides(slide_text)
    print_slide_analysis(slide_results)
        
    # 2. Speech Analysis (v0.2: passing duration_minutes=2.0)
    sample_duration = 2.0
    speech_results = analyze_speech(transcript_text, duration_minutes=sample_duration)
    print_speech_analysis(speech_results, duration_minutes=sample_duration)
        
    # 3. Alignment Analysis
    alignment_results = calculate_alignment(slide_text, transcript_text)
    slide_alignment_results = calculate_slide_wise_alignment(slide_results['slides'], transcript_text)
    print_alignment_analysis(alignment_results, slide_alignment_results)
            
    # 4. Coaching Feedback Generator (v0.5)
    coaching_results = generate_feedback(speech_results, alignment_results, slide_alignment_results)
    print_feedback_summary(coaching_results)
        
    # 5. Feedback Critic (v0.6)
    critic_results = critique_feedback(coaching_results, slide_alignment_results, speech_results)
    print_critic_report(critic_results)
    
    # 6. Viva Question Generator (v0.8)
    viva_questions = generate_viva_questions(slide_results, slide_alignment_results)
    print_viva_questions(viva_questions)
    
    # Print Footer Section
    print_footer()

if __name__ == "__main__":
    run_starter_pipeline()
