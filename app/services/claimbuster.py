import re
from typing import List

import httpx
from app.core.config import settings
from app.schemas.claimbuster import SentenceScore

def _normalize_text_for_claimbuster(text: str) -> str:
    """
    ClaimBuster batch endpoint expects sentences ending with a period.
    """
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text
    # If it ends with ! or ?, converting to .
    if text.endswith(("!", "?")):
        return text[:-1] + "."
    if not text.endswith("."):
        return text + "."
    return text

async def score_text(input_text: str) -> List[SentenceScore]:
    input_text = _normalize_text_for_claimbuster(input_text)

    headers = {"x-api-key": settings.CLAIMBUSTER_API_KEY}
    payload = {"input_text": input_text}

    timeout = httpx.Timeout(settings.CLAIMBUSTER_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(settings.CLAIMBUSTER_BATCH_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    results: List[SentenceScore] = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                sent = item.get("sentence") or item.get("text") or ""
                score = item.get("score") or item.get("checkworthiness") or item.get("value")
                if sent and isinstance(score, (int, float)):
                    results.append(SentenceScore(sentence=sent, score=float(score)))

    elif isinstance(data, dict):
        if "results" in data and isinstance(data["results"], list):
            for item in data["results"]:
                if isinstance(item, dict):
                    sent = item.get("sentence") or item.get("text") or ""
                    score = item.get("score") or item.get("checkworthiness") or item.get("value")
                    if sent and isinstance(score, (int, float)):
                        results.append(SentenceScore(sentence=sent, score=float(score)))
        else:
            # mapping form: { "sentence": 0.87, ... }
            for k, v in data.items():
                if isinstance(k, str) and isinstance(v, (int, float)):
                    results.append(SentenceScore(sentence=k, score=float(v)))

    return results
