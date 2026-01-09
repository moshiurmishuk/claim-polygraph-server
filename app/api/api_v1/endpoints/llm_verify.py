from fastapi import APIRouter, HTTPException, status

from app.schemas.llm_verify import LLMVerifyRequest, LLMVerifyResponse
from app.services.llm_verify import llm_verify_paragraph

router = APIRouter(prefix="/llm", tags=["LLM Claim Verification"])

@router.post("/verify", response_model=LLMVerifyResponse)
async def verify_with_llm(payload: LLMVerifyRequest):
    try:
        data = await llm_verify_paragraph(
            input_text=payload.input_text,
            top_n=payload.top_n,
            min_sources=payload.min_sources,
        )

        # If parsing failed, return raw (still 200)
        if data.get("_parse_error"):
            return LLMVerifyResponse(
                claims=[],
                overall_reliability=None,
                raw=data.get("raw"),
            )

        return LLMVerifyResponse(
            claims=data.get("claims", []),
            overall_reliability=data.get("overall_reliability"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM verification failed: {str(e)}",
        )
