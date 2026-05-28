# PitchPilot: Technical & Presentation Coach Course Notes

These notes outline the key scientific, behavioral, and technical concepts integrated into the PitchPilot scoring and feedback engine.

---

## 🎙️ 1. Speech Delivery & Filler Word Analytics

### The Science of Filler Words
Filler words (disfluencies) like *uh*, *um*, *like*, *so*, and *basically* are natural cognitive pauses. They occur when a speaker's speech rate exceeds their cognitive planning speed. However, high rates of disfluencies decrease perceived credibility, authority, and clarity.

*   **Target Metric:** Ideally < 2-3 filler words per minute.
*   **Pacing (Words Per Minute - WPM):**
    *   *Too Slow:* < 110 WPM (can bore the audience).
    *   *Optimal:* 120 - 150 WPM (conversational, professional).
    *   *Too Fast:* > 160 WPM (makes the speaker sound nervous or rushed).

### Detection Algorithm
PitchPilot scans the transcript text using a sliding-window tokenizer and regex filters to capture:
1.  **Strict Fillers:** `um`, `uh`, `ah`
2.  **Verbal Crutches:** `like`, `so`, `basically`, `actually`, `you know`
3.  **Repetitions:** Consecutive duplicate words (e.g., "the the", "we we")

---

## 📊 2. Slide Design Principles (The "6x6" & Cognitive Load)

Presentation slides are visual aids, not teleprompters. PitchPilot evaluates slide text based on:

### Cognitive Load Theory (Sweller, 1988)
Audiences cannot read dense text and listen to a presenter simultaneously without experiencing cognitive overload (split-attention effect). 

*   **The 6x6 Rule:** A maximum of 6 bullet points per slide, and 6 words per bullet.
*   **Visual Anchor Ratio:** Slides should contain a high ratio of structural/visual cues relative to plain sentences.
*   **Text Density Score:** Measured using word count and character count per slide. Anything exceeding 80 words per slide triggers a "high density / reduce text" recommendation.

---

## 🧠 3. Slide-Speech Semantic Alignment Score

To ensure that the presenter is actually discussing the contents of their current slide, PitchPilot calculates an **Alignment Score** using Sentence Embeddings.

### Mathematical Formulation
1.  Let the slide content text be $S$ and the corresponding speech transcript segment be $T$.
2.  Compute dense vector embeddings using a pre-trained sentence transformer (e.g., SBERT):
    $$\mathbf{v}_S = \text{Embed}(S), \quad \mathbf{v}_T = \text{Embed}(T)$$
3.  Calculate the Cosine Similarity ($\text{Sim}$):
    $$\text{Sim}(S, T) = \frac{\mathbf{v}_S \cdot \mathbf{v}_T}{\|\mathbf{v}_S\| \|\mathbf{v}_T\|}$$
4.  **Interpretation:**
    *   **Score >= 0.75:** Excellent alignment. The spoken explanation matches the slide bullet points.
    *   **Score 0.50 - 0.74:** Moderate alignment. Some deviation or improvisation.
    *   **Score < 0.50:** Poor alignment. Presenter might be talking about a different topic, reading off another slide, or went completely off-script.

---

## 🤖 4. Agentic Feedback Loop (Critic Pattern)

In multi-agent systems, individual specialized agents can produce conflicting or redundant recommendations. PitchPilot applies the **Critic Pattern**:

1.  **Drafting Phase:** The Slide, Speech, and Alignment agents write their observations into the state.
2.  **Critique Phase:** The Critic Agent reads the compiled feedbacks:
    *   Removes duplicate comments.
    *   Checks for logical contradictions.
    *   Formats the final output as a cohesive, structured coaching dashboard.
