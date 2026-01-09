from pydantic import BaseModel, Field
from typing import List, Literal, Optional

Verdict = Literal["True", "False", "Misleading", "Unverified"]

class LLMVerifyRequest(BaseModel):
    input_text: str = Field(..., min_length=1)
    top_n: int = Field(default=3, ge=1, le=10)
    min_sources: int = Field(default=2, ge=1, le=10)

class LLMClaim(BaseModel):
    rank: int
    sentence: str
    verdict: Verdict
    confidence: int
    confidence_band: str
    reasoning: str
    sources: List[str]

class LLMOverallReliability(BaseModel):
    score: int
    band: str
    summary: str

class LLMVerifyResponse(BaseModel):
    provider: Literal["llm_with_search"] = "llm_with_search"
    claims: List[LLMClaim]
    overall_reliability: Optional[LLMOverallReliability] = None
    raw: Optional[str] = None
