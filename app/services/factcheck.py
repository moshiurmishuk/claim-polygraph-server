from typing import List, Optional
import httpx

from app.core.config import settings
from app.schemas.factcheck import FactCheckMatch, FactCheckReview

async def search_fact_checks(
    query: str,
    language: str = "en",
    page_size: int = 3,
) -> List[FactCheckMatch]:
    params = {
        "query": query,
        "languageCode": language,
        "pageSize": page_size,
        "key": settings.FACT_CHECK_API_KEY,
    }

    timeout = httpx.Timeout(settings.FACTCHECK_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(settings.FACTCHECK_ENDPOINT, params=params)
        resp.raise_for_status()
        data = resp.json()

    matches: List[FactCheckMatch] = []

    for claim in data.get("claims", []) or []:
        claim_text = claim.get("text") or ""
        claim_date: Optional[str] = claim.get("claimDate")

        reviews: List[FactCheckReview] = []
        for review in claim.get("claimReview", []) or []:
            publisher = (review.get("publisher") or {}).get("name") or "Unknown publisher"
            title = review.get("title") or "No title"
            url = review.get("url") or ""
            rating = review.get("textualRating") or "No rating"
            reviews.append(FactCheckReview(publisher=publisher, title=title, url=url, rating=rating))

        # Only include if we have something useful
        if claim_text and reviews:
            matches.append(FactCheckMatch(claim=claim_text, claim_date=claim_date, reviews=reviews))

    return matches
