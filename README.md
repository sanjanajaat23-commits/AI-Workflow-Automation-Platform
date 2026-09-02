# AI Workflow Automation Platform

Full-stack workflow orchestration platform for **designing, validating, executing, scheduling, and inspecting multi-step automations** through a visual React Flow editor and FastAPI execution engine.

Built to demonstrate practical **backend engineering, workflow orchestration, API design, persistence, observability, and AI integration**.

## Core Workflow

```text
Visual Workflow Builder
        ↓
Frontend Validation
        ↓
FastAPI API
        ↓
Workflow Executor
        ↓
Node Factory
   ┌────┼─────┐
 HTTP  AI   ...
   └────┼─────┘
        ↓
Execution Result
        ↓
History + Node Logs
```

## Key Engineering Features

- Visual workflow builder powered by React Flow
- Connected workflow nodes with automatic layout
- HTTP nodes for external API calls
- AI nodes with local demo mode and optional OpenAI execution
- FastAPI backend with SQLAlchemy persistence
- SQLite local development database
- Workflow validation before execution
- Node-by-node execution with shared workflow context
- Execution history with status and timestamps
- Node-level INFO/ERROR execution logs
- Automatic workflow-state persistence before execution
- APScheduler integration for scheduled automation
- Structured frontend/backend separation
- Environment-based configuration
- Git hygiene for secrets, caches, databases, and build output

## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│              React + TypeScript + React Flow            │
│                                                         │
│ Dashboard │ Builder │ Executions │ Logs                 │
└──────────────────────────┬──────────────────────────────┘
                           │ REST / JSON
                           ▼
┌─────────────────────────────────────────────────────────┐
│                         FastAPI                         │
│              API Routes → Services → Executor           │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
                    Workflow Engine
                           │
                    Node Factory
                    /     |      \
                 HTTP     AI      ...
                           │
                           ▼
                     SQLAlchemy
                           │
                           ▼
                        SQLite
              Workflows / Executions / Logs
```

## How It Works

1. The user creates a workflow on the visual canvas.
2. Nodes are connected to define execution order.
3. Workflow configuration is validated before execution.
4. The frontend saves the workflow through the API.
5. The execution engine creates an execution record.
6. Nodes execute in workflow order and pass context between steps.
7. Each node writes an execution-log record.
8. The run finishes as `completed` or `failed` with output/error information.
9. Execution history and node logs remain available for inspection.

## Example Automation

```text
Start
  ↓
HTTP Request
  ↓
AI Processing
  ↓
HTTP Request
```

AI nodes support a local demo mode so the example workflow can be tested without OpenAI credits.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite 8, React Flow, Axios, React Router |
| Backend | Python 3.13, FastAPI, SQLAlchemy 2, Pydantic |
| Automation | Workflow engine, node factory, APScheduler |
| AI | OpenAI SDK + local demo mode |
| Persistence | SQLite |
| API | REST / JSON, FastAPI OpenAPI docs |

## Engineering Concepts

- REST API design
- Workflow orchestration
- Node-based execution
- Input validation
- Persistent execution state
- Execution logging and error handling
- Service / CRUD separation
- Scheduled automation
- Environment-based configuration
- Frontend/backend integration

## Project Structure

```text
AI-Workflow-Automation-Platform/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routes
│   │   ├── ai/               # AI integrations
│   │   ├── crud/             # Database operations
│   │   ├── models/           # SQLAlchemy models
│   │   ├── nodes/            # Workflow node implementations
│   │   ├── queue/            # Background task infrastructure
│   │   ├── scheduler/        # Scheduling components
│   │   ├── services/         # Application services
│   │   └── workflow_engine/  # Workflow execution/validation
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── workflow/
├── screenshots/
├── .env.example
├── .gitignore
└── README.md
```

## Screenshots

### Dashboard

![AI Workflow Dashboard](screenshots/dashboard.png)

### Visual Workflow Builder

![Workflow Builder](screenshots/workflow-builder.png)

### Execution Logs

The application provides execution-log views showing individual nodes, timestamps, log levels, and messages.

## Run Locally — Windows PowerShell

### Prerequisites

- Python 3.13
- Node.js / npm
- Git

### Backend

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
python -m uvicorn backend.app.main:app --reload --port 8000
```

FastAPI docs:

`http://127.0.0.1:8000/docs`

Demo mode is enabled by default. For real OpenAI execution, configure `DEMO_MODE=false` and `OPENAI_API_KEY` in `backend/.env`.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

The Vite application normally runs at `http://localhost:5173`.

## Verification

Backend syntax check:

```powershell
python -m compileall backend\app
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## Security & Git Hygiene

Never commit API keys or local secrets. The repository is designed to exclude `.env`, virtual environments, `node_modules`, build output, local databases, logs, and caches.

For production use, the platform would additionally need authentication/authorization, secure secret management, rate limiting, durable background workers, monitoring, audit logging, and production infrastructure.

## Current Scope

The core workflow path is implemented and verified locally: visual workflow design, validation, HTTP/AI execution, persistence, scheduling integration, execution history, and node-level logs.

The AI Assistant and Settings navigation areas are intentionally not presented as completed features.

## Portfolio Value

This project demonstrates hands-on experience with **full-stack application architecture, Python/FastAPI backend development, workflow orchestration, API integration, persistent state, scheduling, error handling, execution observability, React/TypeScript, and AI-enabled automation**.
