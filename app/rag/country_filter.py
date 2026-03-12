"""
Extract country from user query or use provided country.
Used by the RAG pipeline for metadata filtering.
"""
import re
from typing import Optional

# Common country names (subset) for simple extraction
COUNTRIES = [
    "Ghana", "Nigeria", "South Africa", "Kenya",
    "Germany", "United Kingdom", "UK", "France", "Netherlands",
    "United States", "USA", "US", "Canada",
]


def extract_country_from_query(query: str) -> Optional[str]:
    """
    Try to infer country from phrases like 'from Ghana', 'in the UK', 'shopping in Germany'.
    Returns None if not found.
    """
    q = query.strip()
    # "from X", "in X", "shopping in X", "shopping from X", "I am in X"
    for c in COUNTRIES:
        if re.search(rf"\b(from|in|shopping\s+in|shopping\s+from|I\s+am\s+in)\s+{re.escape(c)}\b", q, re.I):
            if c in ("UK", "USA", "US"):
                return "United Kingdom" if c == "UK" else "United States"
            return c
    return None


def resolve_country(query: str, provided_country: Optional[str]) -> Optional[str]:
    """Use provided_country if set, else try to extract from query."""
    if provided_country and str(provided_country).strip():
        return str(provided_country).strip()
    return extract_country_from_query(query)
