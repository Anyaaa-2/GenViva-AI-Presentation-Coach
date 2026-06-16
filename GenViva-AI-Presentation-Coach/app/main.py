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

def run_analysis(slide_text: str, transcript: str, duration_minutes: float = None) -> dict:
    """
    Executes the complete GenViva presentation analysis pipeline.
    Returns a structured dictionary containing all intermediate and final results.
    """
    # 1. Slide Analysis
    slide_analysis = analyze_slides(slide_text)
    
    # 2. Speech & Delivery Analysis
    speech_analysis = analyze_speech(transcript, duration_minutes=duration_minutes)
    
    # 3. Alignment Analysis
    overall_alignment = calculate_alignment(slide_text, transcript)
    slide_wise_alignment = calculate_slide_wise_alignment(slide_analysis['slides'], transcript)
    
    # 4. Coaching Feedback Generator (v0.5)
    feedback = generate_feedback(speech_analysis, overall_alignment, slide_wise_alignment)
    
    # 5. Feedback Critic (v0.6)
    critic_report = critique_feedback(feedback, slide_wise_alignment, speech_analysis)
    
    # 6. Viva Question Generator (v0.8)
    viva_questions = generate_viva_questions(slide_analysis, slide_wise_alignment)
    
    return {
        "slide_analysis": slide_analysis,
        "speech_analysis": speech_analysis,
        "overall_alignment": overall_alignment,
        "slide_wise_alignment": slide_wise_alignment,
        "feedback": feedback,
        "critic_report": critic_report,
        "viva_questions": viva_questions
    }

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
        
    # Run the core analysis pipeline
    sample_duration = 2.0
    results = run_analysis(slide_text, transcript_text, duration_minutes=sample_duration)
    
    # Call report formatter functions to print to terminal
    print_header()
    print_slide_analysis(results["slide_analysis"])
    print_speech_analysis(results["speech_analysis"], duration_minutes=sample_duration)
    print_alignment_analysis(results["overall_alignment"], results["slide_wise_alignment"])
    print_feedback_summary(results["feedback"])
    print_critic_report(results["critic_report"])
    print_viva_questions(results["viva_questions"])
    print_footer()

if __name__ == "__main__":
    run_starter_pipeline()
