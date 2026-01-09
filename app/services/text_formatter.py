import re
from typing import Optional


class TextFormatterService:
    """
    Utility service to normalize and sanitize raw text so it is:
    - JSON safe
    - LLM prompt safe
    - API request safe
    """

    @staticmethod
    def to_json_ready(text: Optional[str]) -> str:
        """
        Main entry point.
        Converts any raw input into a clean, JSON-ready string.
        """
        if not text:
            return ""

        text = str(text)

        text = TextFormatterService._normalize_whitespace(text)
        text = TextFormatterService._normalize_quotes(text)
        text = TextFormatterService._remove_control_chars(text)

        return text.strip()

    @staticmethod
    def to_sentence_ready(text: Optional[str]) -> str:
        """
        Ensures text is suitable for sentence-based APIs
        (e.g. ClaimBuster expects sentences ending with '.')
        """
        text = TextFormatterService.to_json_ready(text)

        if not text:
            return text

        # Replace ! or ? at end with .
        if text.endswith(("!", "?")):
            text = text[:-1] + "."

        if not text.endswith("."):
            text += "."

        return text

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """
        - Convert newlines to spaces
        - Collapse multiple spaces
        """
        text = text.replace("\r\n", " ").replace("\n", " ").replace("\t", " ")
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def _normalize_quotes(text: str) -> str:
        """
        Replace smart quotes with standard ASCII quotes
        """
        replacements = {
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "—": "-",
            "–": "-",
        }

        for k, v in replacements.items():
            text = text.replace(k, v)

        return text

    @staticmethod
    def _remove_control_chars(text: str) -> str:
        """
        Remove non-printable/control characters that break JSON
        """
        return re.sub(r"[\x00-\x1f\x7f]", "", text)
