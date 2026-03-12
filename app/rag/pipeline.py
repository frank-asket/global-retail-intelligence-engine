"""
Full RAG pipeline: query → country detection → security guardrails → hybrid retrieval
→ context build → LLM → grounded response. Optional response sanitization.
"""
import os
import re
from dataclasses import dataclass
from typing import Any, Optional

from app.guardrails.prompt_injection import detect_prompt_injection
from app.guardrails.security_filter import check_restricted_data
from app.rag.country_filter import resolve_country
from app.rag.hybrid_search import HybridRetriever
from app.rag.prompt_builder import build_rag_prompt


@dataclass
class RAGResponse:
    response: str
    blocked: bool = False
    block_reason: Optional[str] = None


def _call_llm(prompt: str) -> str:
    """Call OpenAI chat completion. Falls back to context-only summary if no API key."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        return (
            "[No OPENAI_API_KEY set. Set it to use LLM answers.] "
            "Here is the retrieved context you could use to answer the question."
        )
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"[LLM error: {e}] Use the context above to answer."


def _sanitize_response(text: str) -> str:
    """Remove any leaked restricted terms from the model output."""
    bad = ["supplier", "margin", "internal notes", "warehouse", "profit margin"]
    out = text
    for b in bad:
        if b.lower() in out.lower():
            out = re.sub(re.escape(b), "[redacted]", out, flags=re.I)
    return out


def run_rag(
    query: str,
    country: Optional[str] = None,
    top_k: int = 5,
) -> RAGResponse:
    """
    1. Detect country (from query or provided).
    2. Run security guardrails (prompt injection + restricted data).
    3. Hybrid retrieve with country filter.
    4. Build context and send to LLM.
    5. Sanitize response and return.
    """
    # 1. Country
    resolved_country = resolve_country(query, country)

    # 2. Security: prompt injection
    inj = detect_prompt_injection(query)
    if inj.is_injection:
        return RAGResponse(
            response=inj.message or "Request denied.",
            blocked=True,
            block_reason="prompt_injection",
        )

    # 2. Security: restricted data
    sec = check_restricted_data(query)
    if not sec.allowed:
        return RAGResponse(
            response=sec.message or "Request denied.",
            blocked=True,
            block_reason="restricted_data",
        )

    # 3. Retrieve
    retriever = HybridRetriever(top_k=top_k)
    docs = retriever.search(query=query, country=resolved_country, top_k=top_k)

    # 4. Build prompt and call LLM
    prompt = build_rag_prompt(query, docs, resolved_country)
    answer = _call_llm(prompt)

    # 5. Sanitize
    answer = _sanitize_response(answer)

    return RAGResponse(response=answer, blocked=False)
