from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional

SourceType = Literal["plain_text", "web_url", "youtube_url"]


class TextExtractRequest(BaseModel):
    input: str = Field(
        ...,
        min_length=1,
        description="Plain text OR a URL (web article or YouTube link)",
    )


class TextExtractResponse(BaseModel):
    source_type: SourceType
    text: str
    json_ready_text: str
    analysis: Dict[str, Any]
    warnings: List[str] = []
    metadata: Optional[Dict[str, Any]] = None
