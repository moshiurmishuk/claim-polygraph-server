from typing import Any, Dict, List, Tuple

from app.services.text_formatter import TextFormatterService

from app.processor.processor import process_input, is_url, is_youtube
from app.processor.yt_transcript_fetcher import (
    extract_video_id,
    get_youtube_transcript_any,
)


def _source_type(user_input: str) -> str:
    s = (user_input or "").strip()
    if not s:
        return "plain_text"
    if is_url(s):
        return "youtube_url" if is_youtube(s) else "web_url"
    return "plain_text"


async def extract_text(
    user_input: str,
) -> Tuple[str, str, str, Dict[str, Any], List[str], Dict[str, Any] | None]:
    """
    Returns:
    (source_type, text, json_ready_text, analysis, warnings, metadata)
    """
    src = _source_type(user_input)
    warnings: List[str] = []
    metadata: Dict[str, Any] | None = None

    # Core extraction (your existing pipeline)
    text, analysis, extracted_warnings = process_input(user_input)
    warnings.extend(extracted_warnings or [])

    # Extra metadata for YouTube
    if src == "youtube_url":
        try:
            vid = extract_video_id(user_input)
            meta = get_youtube_transcript_any(vid)

            metadata = {"video_id": vid}
            if meta and isinstance(meta, dict):
                metadata["language_code"] = meta.get("language_code")
        except Exception:
            warnings.append(
                "Could not derive YouTube metadata (video_id/language)."
            )

    # ✅ JSON / LLM safe formatting
    json_ready_text = TextFormatterService.to_json_ready(text)

    return src, text, json_ready_text, analysis, warnings, metadata
