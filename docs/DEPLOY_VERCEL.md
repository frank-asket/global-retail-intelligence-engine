# Deploy to Vercel

The FastAPI backend can be deployed to Vercel as a serverless function. The **vector index** (`data/processed/`, `vector_store/`) is bundled with the deployment so retrieval works without an external database.

## Steps

### 1. Connect the repo

- Go to [vercel.com](https://vercel.com) → **Add New** → **Project**.
- Import your GitHub repo `global-retail-intelligence-engine`.
- Leave **Build Command** and **Output Directory** empty (Vercel detects the FastAPI app).

### 2. Set environment variables

In the project → **Settings** → **Environment Variables**, add:

| Name | Value | Notes |
|------|--------|--------|
| `OPENROUTER_API_KEY` | Your key from [openrouter.ai/keys](https://openrouter.ai/keys) | Required for LLM answers |
| `OPENROUTER_MODEL` | e.g. `openai/gpt-4o-mini` | Optional; default is above |

Apply to **Production**, **Preview**, and **Development** if you use them.

### 3. Deploy

- Click **Deploy**. Vercel will install dependencies from `requirements.txt` and deploy the app at `app/index.py`.
- Your API will be at `https://<your-project>.vercel.app`.
  - Health: `GET https://<your-project>.vercel.app/health`
  - Chat: `POST https://<your-project>.vercel.app/api/chat` with body `{"query": "...", "country": "Ghana"}`.

### 4. Use the chat UI

The **Streamlit** app (`frontend/chat_app.py`) is not hosted on Vercel. To use it:

- Run it locally and point it at your Vercel API:
  ```bash
  export STREAMLIT_CHAT_API_URL=https://<your-project>.vercel.app
  streamlit run frontend/chat_app.py
  ```
- Or build a small static/Next.js chat page and deploy that to Vercel too, with the API URL set to your backend.

## Limits and fallback

- **500 MB** – The deployment bundle (app + dependencies + `data/processed` + `vector_store`) must stay under Vercel’s 500 MB limit. If you hit it, remove optional files in `.vercelignore` or host the index elsewhere.
- **Cold starts** – First request after idle can be slow (loading models and index). Consider keeping the function warm or using a plan with longer timeouts.
- **If deploy fails** (size/timeout) – Host the FastAPI app on [Railway](https://railway.app), [Render](https://render.com), or [Fly.io](https://fly.io), then point your frontend (or Streamlit) at that URL instead.
