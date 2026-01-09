import json
from typing import Any, Dict, Tuple

from app.core.config import settings

from app.llm.prompt_builder import build_factcheck_prompt
from app.llm.llm_inference import generate_response_with_search



def _safe_json_loads(text: str) -> Tuple[Dict[str, Any] | None, str | None]:
    """
    parse JSON even if the model adds extra text.
    Returns (parsed_json, error_message).
    """
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        # Try to extract the first {...} block
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            try:
                return json.loads(candidate), None
            except json.JSONDecodeError as e:
                return None, f"JSON decode error after extraction: {e}"
        return None, "JSON decode error (no JSON object found)"


async def llm_verify_paragraph(input_text: str, top_n: int, min_sources: int) -> Dict[str, Any]:
    prompt = build_factcheck_prompt(
        paragraph=input_text,
        min_sources=min_sources,
        output_format="json",
        include_overall_summary=True,
        top_n=top_n,
    ) 

    
    output_text = generate_response_with_search(prompt)

    parsed, err = _safe_json_loads(output_text)
    if parsed is None:
        # Return minimal structure with raw output
        return {"claims": [], "overall_reliability": None, "raw": output_text, "_parse_error": err}

    # Ensure keys exist
    parsed.setdefault("claims", [])
    parsed.setdefault("overall_reliability", None)
    parsed["_raw"] = None
    return parsed
