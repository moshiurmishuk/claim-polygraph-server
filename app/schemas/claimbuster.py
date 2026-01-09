from pydantic import BaseModel, Field
from typing import List, Literal

class ClaimBusterScoreRequest(BaseModel):
    input_text: str = Field(..., min_length=1, description="Text to score. ClaimBuster expects sentences ending with '.'")

class SentenceScore(BaseModel):
    sentence: str
    score: float

class ClaimBusterScoreResponse(BaseModel):
    provider: Literal["claimbuster"] = "claimbuster"
    results: List[SentenceScore]
