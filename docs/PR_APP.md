# PR: App — documentation and updates

Use this when opening or updating the Pull Request for the **app** package.

---

## PR Title

```
App: docs, package description, and RAG pipeline improvements
```

Or shorter:

```
Document app package and update RAG pipeline
```

---

## PR Description (copy-paste)

### Summary
- Add **app-level documentation** (`app/README.md`) describing the backend: API, RAG pipeline, hybrid retrieval, guardrails, and country handling.
- Add **package docstring** in `app/__init__.py` with a short overview and pointer to the README.
- Add **Vercel entrypoint** (`app/index.py`) so the FastAPI app can be deployed serverlessly.
- **RAG pipeline / retrieval**: refinements and any new modules (e.g. intent classification, metadata filtering, query decomposition/reformulation) as implemented.

### What changed
| Area | Changes |
|------|--------|
| **app/** | `README.md` (what was done here), `__init__.py` (docstring), `index.py` (Vercel). |
| **app/rag/** | Pipeline, hybrid search, prompt builder, country filter; optional new modules (intent classifier, metadata filter, query decomposition/reformulation) if included. |

### How to verify
- Run API: `uvicorn app.main:app --reload`
- Health: `GET /health`
- Chat: `POST /api/chat` with `{"query": "Solar Inverter price in Ghana?", "country": "Ghana"}`
- See `app/README.md` for full flow and module roles.

### Related
- Supports deployment (Vercel) via `app/index.py`.
- Complements project docs (CONTRIBUTING, PRESENTATION_ROADMAP) and main README.
