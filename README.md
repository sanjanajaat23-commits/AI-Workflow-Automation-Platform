## Recommended Python

Use Python 3.13 for local development.

# AI Workflow Automation Platform

A local full-stack workflow automation platform with a React Flow editor, FastAPI backend, SQLite persistence, configurable HTTP/AI nodes, execution history, logs, and a background scheduler.

## Stack

- Frontend: React 19 + TypeScript + Vite 8
- Workflow editor: React Flow
- Backend: FastAPI 0.139.2 + SQLAlchemy 2
- Database: SQLite (local development)
- Scheduler: APScheduler
- AI: OpenAI SDK

## Run locally on Windows PowerShell

### 1. Backend

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
python -m uvicorn backend.app.main:app --reload --port 8000
```

Backend docs: http://127.0.0.1:8000/docs

AI nodes run in local demo mode by default, so no OpenAI key or credits are required. Set `DEMO_MODE=false` and add `OPENAI_API_KEY` to `backend\.env` only if you want real OpenAI execution.

### 2. Frontend

Open a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

## Workflow behavior

- Opening the Workflow Builder automatically creates a local development workflow if none exists.
- The builder uses the real workflow ID returned by the backend; there is no hard-coded workflow ID.
- Execute always saves the current node configuration and connections before running.
- HTTP nodes require a non-empty URL before execution.
- AI nodes require a prompt. They run in demo mode by default; set `DEMO_MODE=false` and configure `OPENAI_API_KEY` for real model execution.
- Unsupported node types are not exposed in the palette until their backend implementations are ready.

## GitHub hygiene

The repository ignores virtual environments, `node_modules`, build output, local `.env` files, databases, logs, and caches. Commit `backend\.env.example`, never `backend\.env`.

## Verification

Backend Python files can be syntax-checked with:

```powershell
python -m compileall backend\app
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## Local environment
Create `backend/.env` from `backend/.env.example`. Demo mode is enabled by default. For real OpenAI execution, set `DEMO_MODE=false` and add `OPENAI_API_KEY`. Never commit `backend/.env`.
