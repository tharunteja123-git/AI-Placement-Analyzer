# AI Placement Analyzer

## Run locally

Start the FastAPI backend from `backend/`:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Start the Next.js frontend in a second terminal from `frontend/`:

```powershell
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Next.js proxies `/api/*` requests to `http://127.0.0.1:8000` by default. Set `BACKEND_API_URL` before starting Next.js to use a different backend address.
