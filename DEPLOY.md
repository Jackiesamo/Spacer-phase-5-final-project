Deployment guide — Frontend to Vercel, Backend to Render
===============================================

This repository contains a Vite React frontend (`/frontend`) and a FastAPI backend (`/backend`). The recommended deployment is:

- Frontend: Vercel (the repo already contains `vercel.json`)
- Backend: Render (managed Postgres)

What I added
- `backend/Dockerfile` — container for the backend (used locally or by Render)
- `backend/requirements.txt` — minimal Python dependencies
- `docker-compose.yml` — local development stack (Postgres + backend)
- `render.yaml` — manifest to create a Render web service + managed Postgres
- `.github/workflows/deploy-backend.yml` — CI that installs deps, runs backend tests, and triggers a Render deploy when `RENDER_API_KEY` and `RENDER_SERVICE_ID` are present

Required secrets / env vars

- For Render service (set in Render dashboard or via the manifest):
  - DATABASE_URL (Render will set this automatically for managed DB)
  - SECRET_KEY
  - ALGORITHM (e.g. HS256)
  - ACCESS_TOKEN_EXPIRE_MINUTES (e.g. 30)

- For GitHub Actions (optional, only needed if you want Actions to trigger Render deploys):
  - `RENDER_API_KEY` — your Render API key
  - `RENDER_SERVICE_ID` — ID of the Render service (found in Render dashboard or API)
  - `RENDER_DB_URL` — (optional) direct DB URL to run migrations from Actions
  - `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` — (optional) for Actions-based Vercel deploys

Quick local test

1. Start the local stack:

```bash
docker-compose up --build
```

2. Open http://localhost:8000/ — the backend should respond at `/`

Connecting Vercel (frontend)

If your repository is connected to Vercel, pushes to the branch will trigger Vercel builds automatically. The existing `vercel.json` should be sufficient for a standard Vite build.

Connecting Render (backend)

Option A (recommended): Connect your GitHub repo in the Render dashboard and create a new Web Service using the `backend/` root, or import the provided `render.yaml`.

Option B: Use GitHub Actions to trigger deploys. Create two repository secrets: `RENDER_API_KEY` and `RENDER_SERVICE_ID`. The workflow will trigger a deploy after successful checks.

Running migrations

After Render provisions the managed Postgres, run Alembic migrations. You can either run them as a one-off job on Render or run them locally using the connection string provided by Render.

Example (locally):

```bash
# set DATABASE_URL to the Render postgres URL
export DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
cd backend
alembic upgrade head
```

If you'd like, I can also add a GitHub Action step that runs Alembic migrations automatically against the Render DB (requires a DB connection string secret).

Note: I added a dedicated `migrations.yml` workflow that will run Alembic when `RENDER_DB_URL` is set as a repo secret; this can be triggered manually from the Actions tab or run on push.
Next steps I can take for you

- Wire up a Render one-off task to run migrations automatically on deploy
- Add a small healthcheck endpoint and readiness probe in the Render manifest
- Add a GitHub Actions job to build and deploy the frontend to Vercel (if you prefer Actions instead of Vercel's GitHub integration)
