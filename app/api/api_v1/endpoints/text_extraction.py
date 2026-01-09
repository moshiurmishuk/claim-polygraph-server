from fastapi import APIRouter, HTTPException, status

from app.schemas.text_extraction import (
    TextExtractRequest,
    TextExtractResponse,
)
from app.services.text_extraction import extract_text

router = APIRouter(prefix="/text", tags=["Text Extraction"])


@router.post("/extract", response_model=TextExtractResponse)
async def text_extraction(payload: TextExtractRequest):
    try:
        (
            source_type,
            text,
            json_ready_text,
            analysis,
            warnings,
            metadata,
        ) = await extract_text(payload.input)

        return TextExtractResponse(
            source_type=source_type,
            text=text,
            json_ready_text=json_ready_text,
            analysis=analysis,
            warnings=warnings,
            metadata=metadata,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}",
        )
