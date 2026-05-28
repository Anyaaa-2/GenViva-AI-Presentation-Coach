# PitchPilot: Agentic AI Presentation Coach 🚀

PitchPilot is a multimodal, human-centered AI presentation coaching system designed to help students, researchers, and professionals deliver flawless presentations. By analyzing both the **presentation slides** and the **speech transcripts** (or spoken delivery), PitchPilot provides real-time, slide-wise feedback, delivery analytics, viva question preparation, and a slide-speech alignment score.

This is a placement-ready project implementing an **agentic workflow** with a feedback-critic pattern to ensure high-quality, actionable presentation recommendations.

---

## 📌 Features

### 1. Slide-Wise Feedback
- Extracts content structure, readability, slide density, and bullet-point conciseness.
- Evaluates the design layout recommendations and suggests visual improvements.

### 2. Speech & Delivery Analytics
- Analyzes speech transcripts for pacing (words per minute), tone, and clarity.
- Identifies filler words (e.g., *um*, *ah*, *like*, *basically*) and provides frequency distribution charts.

### 3. Slide-Speech Alignment
- Cross-modal analysis comparing what is on the slides with what is spoken.
- Provides a semantic similarity score to determine if the presenter strayed off-topic or forgot to talk about key slide points.

### 4. Viva Question Generator
- Dynamically generates potential viva/QA questions that examiners might ask based on the presentation content.
- Drafts sample model answers for preparation.

### 5. Agentic Feedback Critic
- Implements an iterative critic agent that reviews feedback from the individual coaches to ensure recommendations are not contradictory, are constructive, and are actionable.

### Current Progress - v0.1 Starter Pipeline

The starter version currently supports:
- **Slide Text Splitting & Slide Count:** Splits slide text into individual slides and counts them.
- **Speech Transcript Word Count:** Calculates the total word count from spoken transcripts.
- **Filler Word Detection & Distribution:** Identifies common filler words and maps their frequency.
- **Basic Slide-Speech Alignment Score:** Computes a simple word-overlap alignment score between slide text and transcript.
- **Local Execution:** Can be run locally using the command `python app/main.py`.

---


## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit (For rich user dashboards, analytics visualization, and upload controls)
- **Backend API:** FastAPI (For backend services and orchestration endpoints)
- **Orchestration & Agents:** LangChain, LangGraph (For stateful multi-agent workflows)
- **Speech-to-Text:** Faster-Whisper (For localized high-performance audio transcription)
- **Embedding & Vector Search:** Sentence Transformers, FAISS (For semantic comparison and alignment scores)
- **Data Analytics:** NumPy, pandas, Matplotlib, Seaborn (For visualization of filler words and delivery statistics)

---

## 📂 Project Structure

```text
PitchPilot-AI-Presentation-Coach/
├── app/
│   ├── main.py                 # FastAPI / Streamlit entry point
│   ├── slide_analyzer.py       # Slide text analysis logic
│   ├── speech_analyzer.py      # Speech transcript & filler word logic
│   ├── alignment_analyzer.py   # Slide-speech semantic alignment scoring
│   ├── viva_generator.py       # Viva question generation engine
│   └── feedback_critic.py      # Multi-agent consensus & critique layer
├── data/
│   └── sample_inputs/
│       ├── sample_slide_text.txt
│       └── sample_transcript.txt
├── docs/
│   ├── architecture.md         # Detailed design, workflow & Agent schema
│   └── course-notes.md         # Academic and theoretical background
├── notebooks/                  # Experimental notebooks (prototyping)
├── README.md                   # This project index
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules
```

---

## 🚀 Getting Started

*(Note: Dependencies installation should be done in a virtual environment.)*

### 1. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
*(Starter skeleton is ready. Run main application once endpoints are fully wired.)*
```bash
python app/main.py
```

---

## 🏛️ Architecture & Agent Workflow

PitchPilot uses a **Stateful Multi-Agent System** powered by LangGraph:

1. **Slide Analyzer Agent:** Extracts slide structure and drafts slide feedback.
2. **Speech Coach Agent:** Analyzes the verbal delivery structure and counts filler words.
3. **Alignment Agent:** Checks semantic alignment between slide text and spoken words.
4. **Viva Question Agent:** Creates custom viva questions based on weak spots and presentation claims.
5. **Feedback Critic Agent:** Synthesizes the outputs, removes redundancies, and refines the tone.

For a detailed breakdown, please read the [Architecture Documentation](docs/architecture.md).
