from fastapi import APIRouter, HTTPException, status
import httpx

from app.schemas.factcheck import (
    FactCheckVerifyRequest,
    FactCheckVerifyResponse,
    FactCheckSentenceResult,
)
from app.services.factcheck import search_fact_checks

router = APIRouter(prefix="/factcheck", tags=["Fact Check"])

@router.post("/verify", response_model=FactCheckVerifyResponse)
async def verify_claims(payload: FactCheckVerifyRequest):
    try:
        results = []
        for sentence in payload.sentences:
            matches = await search_fact_checks(
                query=sentence,
                language=payload.language,
                page_size=payload.page_size,
            )
            results.append(FactCheckSentenceResult(sentence=sentence, matches=matches))

        return FactCheckVerifyResponse(results=results)

    except httpx.HTTPStatusError as e:
        # Google API returned 4xx/5xx
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Google Fact Check error: {e.response.status_code} - {e.response.text[:300]}",
        )
    except httpx.RequestError as e:
        # Network / timeout / DNS
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Google Fact Check request failed: {str(e)}",
        )
