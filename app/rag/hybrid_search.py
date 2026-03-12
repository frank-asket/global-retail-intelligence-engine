"""
Hybrid retriever: FAISS vector search + BM25 keyword search with metadata (country) filtering.
Returns top-k results, optionally filtered by country.
"""
import json
from pathlib import Path
from typing import Any, Optional

import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# Default index path relative to project root
def _default_index_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "vector_store" / "faiss_index"


class HybridRetriever:
    def __init__(
        self,
        index_dir: Optional[Path] = None,
        model_name: str = "all-MiniLM-L6-v2",
        top_k: int = 5,
    ):
        self.index_dir = index_dir or _default_index_path()
        self.model_name = model_name
        self.top_k = top_k
        self._index: Optional[faiss.Index] = None
        self._metadata: list[dict[str, Any]] = []
        self._model: Optional[SentenceTransformer] = None
        self._bm25: Optional[BM25Okapi] = None
        self._tokenized_corpus: Optional[list[list[str]]] = None

    def _ensure_loaded(self) -> None:
        if self._index is not None:
            return
        if not self.index_dir.exists():
            raise FileNotFoundError(
                f"Vector index not found at {self.index_dir}. Run scripts/run_indexing.py first."
            )
        self._index = faiss.read_index(str(self.index_dir / "index.faiss"))
        with open(self.index_dir / "metadata.json", "r", encoding="utf-8") as f:
            self._metadata = json.load(f)
        self._model = SentenceTransformer(self.model_name)
        # BM25 on searchable_text
        corpus = [m.get("searchable_text", "") for m in self._metadata]
        self._tokenized_corpus = [doc.lower().split() for doc in corpus]
        self._bm25 = BM25Okapi(self._tokenized_corpus)

    def _filter_by_country(self, indices: list[int], country: Optional[str]) -> list[int]:
        if not country or not country.strip():
            return indices
        country_lower = country.strip().lower()
        return [
            i for i in indices
            if self._metadata[i].get("country", "").lower() == country_lower
        ]

    def search(
        self,
        query: str,
        country: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """
        Run hybrid search (vector + BM25), optionally filter by country.
        Returns list of metadata dicts with score, ordered by relevance.
        """
        k = top_k or self.top_k
        self._ensure_loaded()

        # Vector search
        q_emb = self._model.encode([query])
        q_emb = np.array(q_emb, dtype=np.float32)
        faiss.normalize_L2(q_emb)
        vector_k = min(k * 3, len(self._metadata))  # over-fetch for filtering
        scores_vec, indices_vec = self._index.search(q_emb, vector_k)
        indices_vec = indices_vec[0].tolist()
        scores_vec = scores_vec[0].tolist()

        # BM25 search
        tokenized_query = query.lower().split()
        bm25_scores = self._bm25.get_scores(tokenized_query)
        order_bm25 = np.argsort(bm25_scores)[::-1][: vector_k]
        indices_bm25 = order_bm25.tolist()
        scores_bm25_list = bm25_scores.tolist()

        # Normalize BM25 to [0,1] for fusion (avoid div by zero)
        max_bm = max(scores_bm25_list) or 1.0
        scores_bm25_norm = [s / max_bm for s in scores_bm25_list]

        # Reciprocal rank fusion: score = 1/(rank_vec) + 1/(rank_bm25)
        rank_vec = {idx: r for r, idx in enumerate(indices_vec, 1)}
        rank_bm25 = {int(idx): r for r, idx in enumerate(indices_bm25, 1)}
        all_indices = set(indices_vec) | set(indices_bm25)
        fused = []
        for idx in all_indices:
            rv = rank_vec.get(idx, 1000)
            rb = rank_bm25.get(idx, 1000)
            fused.append((idx, 1.0 / rv + 1.0 / rb))
        fused.sort(key=lambda x: -x[1])

        # Apply country filter and take top_k
        ordered_indices = [idx for idx, _ in fused]
        filtered = self._filter_by_country(ordered_indices, country)
        if not filtered and country:
            # Fallback: return top fused without country filter so we don't return empty
            filtered = ordered_indices[:k]
        else:
            filtered = filtered[:k] if filtered else ordered_indices[:k]

        results = []
        for idx in filtered:
            meta = dict(self._metadata[idx])
            meta["score"] = next(s for i, s in fused if i == idx)
            results.append(meta)
        return results
