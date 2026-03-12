# Next.js Frontend

The **Next.js** app in `web/` is a chat UI for the Global Retail Intelligence Engine. It works with the FastAPI backend and is ideal for deploying on **Vercel**.

## Run locally

1. **Start the FastAPI backend** (from the project root):
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Install and run the Next.js app**:
   ```bash
   cd web
   npm install
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000). The app calls `http://localhost:8000` by default.

## Environment variable

Set the backend URL for production or a different host:

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_CHAT_API_URL` | Base URL of the FastAPI backend (e.g. `https://your-api.vercel.app` or `https://your-app.railway.app`) |

- **Local:** Default is `http://localhost:8000` if unset.
- **Vercel:** In Project → Settings → Environment Variables, add `NEXT_PUBLIC_CHAT_API_URL` = your backend URL.

Create `web/.env.local` for local overrides:

```
NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000
```

## Deploy the Next.js app to Vercel

1. In [Vercel](https://vercel.com) → **Add New** → **Project** → Import your repo.
2. Set **Root Directory** to `web` (so Vercel builds the Next.js app).
3. Add environment variable: `NEXT_PUBLIC_CHAT_API_URL` = your FastAPI backend URL (e.g. your other Vercel deployment or Railway/Render).
4. Deploy.

Your chat UI will be at `https://<your-project>.vercel.app` and will use the backend you configured.

## Stack

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- No extra UI library; styling is in `app/globals.css`.
