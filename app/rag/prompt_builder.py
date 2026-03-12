"""
Build the RAG prompt: system + context (retrieved docs) + user query for the LLM.
"""
from typing import Any


def build_rag_prompt(
    query: str,
    context_docs: list[dict[str, Any]],
    country: str | None = None,
) -> str:
    """
    Assemble system instructions, retrieved context, and user query.
    Context is formatted from hybrid search results (item_name, price, specs, etc.).
    """
    lines = [
        "You are a helpful retail assistant for GlobalCart. Answer only using the provided product and policy context. "
        "If the answer is not in the context, say you don't have that information. "
        "Never mention suppliers, margins, internal notes, or warehouse details."
    ]
    if country:
        lines.append(f"User region: {country}. Use only pricing and availability for this region.")
    lines.append("")
    lines.append("--- Context ---")
    for i, doc in enumerate(context_docs[:5], 1):
        parts = [
            f"Product: {doc.get('item_name', '')}",
            f"ID: {doc.get('product_id', '')}",
            f"Country: {doc.get('country', '')}",
            f"Price: {doc.get('price_local', '')} {doc.get('currency', '')}",
            f"Specs: {doc.get('technical_specs', '')}",
        ]
        lines.append("\n".join(parts))
        lines.append("")
    lines.append("--- End context ---")
    lines.append("")
    lines.append(f"User question: {query}")
    lines.append("Answer:")
    return "\n".join(lines)
