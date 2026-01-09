from fastapi import APIRouter, HTTPException, status
import httpx

from app.schemas.claimbuster import ClaimBusterScoreRequest, ClaimBusterScoreResponse
from app.services.claimbuster import score_text

router = APIRouter(prefix="/claimbuster", tags=["ClaimBuster"])

@router.post("/score", response_model=ClaimBusterScoreResponse)
async def score_claimbuster(payload: ClaimBusterScoreRequest):
    try:
        results = await score_text(payload.input_text)
        return ClaimBusterScoreResponse(results=results)
    except httpx.HTTPStatusError as e:
        # if third-party returned an error (401, 429, 5xx etc.)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"ClaimBuster error: {e.response.status_code} - {e.response.text[:300]}",
        )
    except httpx.RequestError as e:
        # for network error, dns, connection, timeout
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"ClaimBuster request failed: {str(e)}",
        )
