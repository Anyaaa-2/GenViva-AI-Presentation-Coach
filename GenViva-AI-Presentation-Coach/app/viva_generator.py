import re
from typing import Dict, Any, List

def generate_viva_questions(slide_text: str, transcript: str) -> Dict[str, Any]:
    """
    Analyzes content to produce academic/professional viva/QA questions and model answers.
    
    Args:
        slide_text (str): Slide texts.
        transcript (str): Presenter transcript text.
        
    Returns:
        Dict[str, Any]: Structured list of viva questions, conceptual focus, and suggested strategies.
    """
    combined_content = (slide_text + " " + transcript).lower()
    
    # Simple rule-based trigger system to simulate LLM domain question generation
    viva_questions = []
    
    if "anxiety" in combined_content or "problem" in combined_content:
        viva_questions.append({
            "id": 1,
            "question": "What primary source or survey did you base your 75% presentation anxiety statistic on?",
            "ideal_response_keywords": ["reference", "empirical study", "research survey"],
            "difficulty": "Medium",
            "coaching_tip": "Be prepared to cite specific studies or clarify if it represents target audience surveys."
        })
        
    if "langgraph" in combined_content or "agent" in combined_content:
        viva_questions.append({
            "id": 2,
            "question": "Why did you choose a Multi-Agent system (LangGraph) over a single LLM chain for PitchPilot?",
            "ideal_response_keywords": ["statefulness", "critic pattern", "parallel nodes", "specialization"],
            "difficulty": "Hard",
            "coaching_tip": "Highlight that presentation coaching contains conflicting domains (pacing vs content depth) which suit decoupled agent feedback with a feedback critic."
        })
        
    if "whisper" in combined_content or "faster-whisper" in combined_content:
        viva_questions.append({
            "id": 3,
            "question": "How will your system handle real-time audio chunking and latency when using faster-whisper?",
            "ideal_response_keywords": ["vad filter", "sliding window", "local hosting", "concurrency"],
            "difficulty": "Hard",
            "coaching_tip": "Mention Voice Activity Detection (VAD) to split sentences dynamically before sending them for transcription."
        })
        
    if "alignment" in combined_content or "sentence transformer" in combined_content:
        viva_questions.append({
            "id": 4,
            "question": "How does the slide-speech alignment module handle vocabulary mismatch (e.g., synonyms)?",
            "ideal_response_keywords": ["dense embeddings", "semantic similarity", "cosine distance", "not just keyword match"],
            "difficulty": "Medium",
            "coaching_tip": "Explain that Sentence Transformers map words to a joint vector space, capturing semantic meaning rather than exact spelling overlaps."
        })
        
    # Fallback default questions if content is sparse
    if len(viva_questions) < 2:
        viva_questions.append({
            "id": 5,
            "question": "Can you explain the scalability constraints of this system when dealing with larger slideshows?",
            "ideal_response_keywords": ["batch processing", "context length limit", "rate limiting"],
            "difficulty": "Medium",
            "coaching_tip": "Discuss pagination of slides and chunking of audio."
        })

    return {
        "status": "success",
        "total_questions_generated": len(viva_questions),
        "questions": viva_questions
    }

if __name__ == "__main__":
    print(generate_viva_questions("We use LangGraph and Whisper.", "This is our agentic tool."))
