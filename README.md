# Claim-Polygraph-Server

Claim-Polygraph is an automated pipeline for extracting, analyzing, and fact-checking claims from news articles, YouTube videos, and other sources using LLMs and external fact-checking APIs.

## Features

- **Text Extraction**: Extracts readable text from web articles and transcribes spoken content from YouTube videos.
- **Claim Identification**: Uses ClaimBuster API to find the most check-worthy sentences.
- **Claim Extraction**: Extracts concise, verifiable claims from text using LLM prompts.
- **Fact-Checking**:
  - LLM-based fact-checking with standardized scoring and reasoning.
  - Integrates with Google Fact Check Tools API for external fact-check reviews.
- **Web Interface**: Flask-based UI for submitting text or URLs and viewing results.
- **Rich Output**: Displays claim-worthiness scores, fact-check verdicts, confidence bands, sources, and reasoning.

## Usage

- Paste raw text, a news/article URL, or a YouTube video URL into the input box.
- The system will extract text, identify claims, and run fact-checking.
- Results include:
  - Top claim-worthy sentences ([ClaimBuster](https://idir.uta.edu/claimbuster/))
  - LLM-based fact-checks with verdicts, confidence, reasoning, and sources ([OpenAI GPT](https://platform.openai.com/docs/))
  - External fact-check reviews from [Google Fact Check Tools](https://toolbox.google.com/factcheck/explorer)



## APIs Used

- [OpenAI GPT](https://platform.openai.com/docs/)
- [ClaimBuster](https://idir.uta.edu/claimbuster/api/)
- [Google Fact Check Tools](https://developers.google.com/fact-check/tools/api/reference/rest)

---

# Confidence & Reliability Standardization of LLM Fact Checking

To ensure consistent and transparent fact-checking, every claim and overall text assessment follows a standardized scoring rubric.

### Confidence & Reliability Bands (0–100)

| Score Range | Band Label          |
| ----------- | ------------------- |
| 95–100      | Established Fact    |
| 85–94       | Very Likely         |
| 70–84       | Likely              |
| 55–69       | Uncertain / Mixed   |
| 35–54       | Doubtful            |
| 15–34       | Unlikely            |
| 0–14        | False / Unsupported |

### Scoring Checklist

- **Source Quality (SQ):** Primary/official > peer-reviewed > major media > other > blogs/social
- **Independence & Count (IC):** More independent, corroborating sources → higher score
- **Consensus (CS):** Strong agreement among fact-checkers/experts → higher score
- **Recency/Relevance (RR):** Current & relevant evidence → higher score
- **Specificity/Verifiability (SV):** Concrete, measurable, and fact-checkable claims → higher score
- **Conflict (CP):** Credible contradictory evidence reduces score

---

## Scoring Technique & Formula

Each claim’s confidence score is derived using a **deterministic weighted formula**.

### Weights

- SQ (Source Quality): **0.30**
- IC (Independence & Count): **0.20**
- CS (Consensus): **0.20**
- RR (Recency/Relevance): **0.15**
- SV (Specificity/Verifiability): **0.10**
- CP (Conflict Penalty): **−0.15**

### Sub-scores (0–100 scale)

- **SQ:** Official/peer-reviewed (90–100), major media (75–89), mixed/unknown (50–74), blogs/social (0–49)
- **IC:** 3+ sources (95–100), 2 sources (85–94), 1 source (60–79), none (0–40)
- **CS:** Clear alignment (90–100), minor dissent (70–89), mixed (40–69), major dissent (0–39)
- **RR:** ≤12 months (90–100), ≤24 months (75–89), stable but older (60–79), stale (0–59)
- **SV:** Precise (85–100), definition-dependent (60–84), vague (0–59)
- **CP:** None (0), minor (−5 to −8), substantial (−9 to −12), strong contradiction (−13 to −15)

### Formula

```
Score = 100 * (0.30*SQ + 0.20*IC + 0.20*CS + 0.15*RR + 0.10*SV) + CP
```

After computing, scores are **rounded to the nearest integer** and mapped to the confidence bands.

---

## Overall Reliability Assessment

In addition to per-claim verdicts, the system generates an **Overall Reliability Assessment** of the text:

- **Reliability Score (0–100):** Computed using the same weighted rubric and formula.
- **Reliability Band:** Mapped to the same bands as above.
- **Summary Paragraph:** A concise analysis noting:
  - Major strengths (e.g., strong source consensus, official data support)
  - Weaknesses (e.g., lack of sources, outdated evidence, mixed findings)
  - Uncertainty or conflicts across claims
  - Overall trustworthiness of the text

---


## Acknowledgments

- [ClaimBuster](https://idir.uta.edu/claimbuster/)
- [Google Fact Check Tools](https://toolbox.google.com/factcheck/explorer)
- [OpenAI](https://openai.com/)

```

```
