from pydantic import BaseModel, Field
from typing import List, Optional

class FactCheckVerifyRequest(BaseModel):
    sentences: List[str] = Field(..., min_length=1, description="Claim sentences to verify via Google Fact Check Tools API")
    language: str = Field(default="en", description="Language code, e.g., en")
    page_size: int = Field(default=3, ge=1, le=10, description="Max results per sentence")

class FactCheckReview(BaseModel):
    publisher: str
    title: str
    url: str
    rating: str

class FactCheckMatch(BaseModel):
    claim: str
    claim_date: Optional[str] = None
    reviews: List[FactCheckReview]

class FactCheckSentenceResult(BaseModel):
    sentence: str
    matches: List[FactCheckMatch]

class FactCheckVerifyResponse(BaseModel):
    provider: str = "google_factcheck"
    results: List[FactCheckSentenceResult]
