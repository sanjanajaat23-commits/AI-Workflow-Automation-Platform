# AI Workflow Automation Platform

A full-stack workflow automation platform for designing, saving, executing, and inspecting multi-step workflows through a visual React Flow editor and a FastAPI execution engine.

The project demonstrates an end-to-end automation pipeline: **visual workflow design → backend validation → node execution → persistent execution history → node-level execution logs**.

> Built as a portfolio project to demonstrate practical full-stack, backend, workflow-engineering, and AI integration skills.

## Highlights

- Visual workflow builder powered by React Flow
- Connected workflow nodes with automatic layout
- HTTP nodes for external API calls
- AI nodes with local demo mode and optional OpenAI execution
- FastAPI backend with SQLAlchemy persistence
- SQLite local development database
- Workflow validation before execution
- Execution history with status and timestamps
- Node-level execution logs with INFO/ERROR levels
- Automatic saving of workflow configuration before execution
- APScheduler integration for scheduled automation
- Windows PowerShell development workflow

## Screenshots

### Dashboard

![AI Workflow Dashboard](screenshots/dashboard.png)

### Visual Workflow Builder

![Workflow Builder](screenshots/workflow-builder.png)

### Execution Logs

The application also provides a live execution-log view showing the individual nodes executed during a workflow run, including timestamps, log levels, and messages.

## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                     React + TypeScript                  │
│                    Vite + React Flow                    │
│                                                         │
│  Dashboard │ Workflow Builder │ Executions │ Logs      │
└──────────────────────────┬──────────────────────────────┘
                           │ REST / JSON
                           ▼
┌─────────────────────────────────────────────────────────┐
│                       FastAPI                           │
│                                                         │
│  API Routes → Services → Workflow Executor             │
│                         │                               │
│                         ▼                               │
│                 Node Factory / Nodes                    │
│                 HTTP │ AI │ ...                         │
└──────────────────────────┬──────────────────────────────┘
                           │ SQLAlchemy
                           ▼
┌─────────────────────────────────────────────────────────┐
│                        SQLite                           │
│                                                         │
│ Workflows │ Executions │ Execution Logs                 │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend

- React 19
- TypeScript
- Vite 8
- React Flow
- Axios
- React Router

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2
- Pydantic
- SQLite
- APScheduler
- OpenAI SDK

### Engineering Concepts

- REST API design
- Workflow orchestration
- Node-based execution
- Input validation
- Persistent execution state
- Execution logging
- Error handling
- Service/CRUD separation
- Environment-based configuration

## How It Works

1. A user opens the Workflow Builder.
2. Nodes are placed and connected on the React Flow canvas.
3. Node configuration is validated before execution.
4. The frontend saves the current workflow state through the API.
5. The FastAPI workflow executor creates an execution record.
6. Nodes execute in workflow order and pass context between steps.
7. Each executed node creates an execution-log record.
8. The execution is marked `completed` or `failed` with output/error information.
9. Execution history and logs can be inspected from the frontend.

## Example Workflow

```text
Start
  ↓
HTTP Request
  ↓
AI Processing
  ↓
HTTP Request
```

The repository includes a working local workflow using this pattern. In demo mode, AI nodes can execute without requiring OpenAI credits.

## Local Setup — Windows PowerShell

### Prerequisites

- Python 3.13
- Node.js / npm
- Git

### 1. Clone the repository

```powershell
git clone https://github.com/sanjanajaat23-commits/AI-Workflow-Automation-Platform.git
cd AI-Workflow-Automation-Platform
```

### 2. Create and activate the Python environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```

### 3. Configure the backend

```powershell
Copy-Item backend\.env.example backend\.env
```

Demo mode is enabled by default, so an OpenAI API key is not required for the demo workflow.

For real OpenAI execution, configure `backend\.env` with:

```text
DEMO_MODE=false
OPENAI_API_KEY=your_key_here
```

**Never commit `backend/.env`.**

### 4. Start the backend

From the project root:

```powershell
python -m uvicorn backend.app.main:app --reload --port 8000
```

FastAPI docs:

`http://127.0.0.1:8000/docs`

### 5. Start the frontend

Open a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

`http://localhost:5173`

## Verification

### Backend syntax check

From the project root:

```powershell
python -m compileall backend\app
```

### Frontend production build

```powershell
cd frontend
npm run build
```

The production build should complete successfully with TypeScript compilation and Vite bundling.

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
│       ├── components/       # Shared UI components
│       ├── pages/            # Dashboard, executions, logs
│       ├── services/         # API clients
│       └── workflow/         # Visual workflow builder
├── screenshots/
├── .env.example
├── .gitignore
└── README.md
```

## Current Scope

The core workflow automation path is implemented and verified locally. The main supported experience is the visual builder, HTTP/AI workflow execution, execution history, and execution logs.

The AI Assistant and Settings navigation areas are intentionally not presented as completed features.

## GitHub Hygiene

The repository ignores local environments, `node_modules`, build output, `.env` files, local databases, logs, and caches.

Commit `backend/.env.example` for configuration guidance, but never commit `backend/.env` or API keys.

## Why This Project

This project was designed to demonstrate more than a frontend interface. It combines a typed React application with a Python API, persistent state, a workflow execution engine, configurable nodes, validation, error handling, and observable execution history/logging.
