from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# Import Models
# --------------------------------------------------

from backend.app.models.user import User
from backend.app.models.workflow import Workflow
from backend.app.models.workflow_node import WorkflowNode
from backend.app.models.workflow_connection import WorkflowConnection
from backend.app.models.execution import Execution
from backend.app.models.execution_log import ExecutionLog
from backend.app.models.schedule import WorkflowSchedule
from backend.app.database.database import Base, engine, SessionLocal
from backend.app.models.user import User
from backend.app.core.security import hash_password

# --------------------------------------------------
# Register Built-in Nodes
# --------------------------------------------------

from backend.app.nodes import register_builtin_nodes

# --------------------------------------------------
# Scheduler
# --------------------------------------------------

from backend.app.core.scheduler import (
    start_scheduler,
    stop_scheduler,
)

# --------------------------------------------------
# Routers
# --------------------------------------------------

from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.auth.register import router as register_router
from backend.app.api.v1.auth.login import router as login_router
from backend.app.api.v1.workflows import router as workflows_router
from backend.app.api.v1.workflow_nodes import router as workflow_nodes_router
from backend.app.api.v1.workflow_connections import router as workflow_connections_router
from backend.app.api.v1.executions import router as executions_router
from backend.app.api.v1.execution_logs import router as execution_logs_router
from backend.app.api.v1.dashboard import router as dashboard_router
from backend.app.api.v1.schedules import router as schedules_router
from backend.app.api.v1.webhooks import router as webhooks_router
from backend.app.api.v1.workflow_templates import (
    router as workflow_templates_router,
)

app = FastAPI(
    title="AI Workflow Automation Platform",
    description="AI-powered workflow automation platform",
    version="2.3.0",
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Startup / Shutdown
# --------------------------------------------------

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    # Development seed: the current UI uses a temporary user until JWT auth
    # is wired into workflow routes. This keeps a fresh local database usable.
    db = SessionLocal()
    try:
        if db.query(User).filter(User.id == 1).first() is None:
            db.add(
                User(
                    id=1,
                    username="dev",
                    email="dev@example.com",
                    hashed_password=hash_password("dev-password"),
                    is_active=True,
                )
            )
            db.commit()
    finally:
        db.close()

    register_builtin_nodes()
    start_scheduler()


@app.on_event("shutdown")
def shutdown():
    stop_scheduler()


# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    register_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    login_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    workflows_router,
    prefix="/api/v1/workflows",
    tags=["Workflows"],
)

app.include_router(
    workflow_nodes_router,
    prefix="/api/v1/workflows",
    tags=["Workflow Nodes"],
)

app.include_router(
    workflow_connections_router,
    prefix="/api/v1/workflows",
    tags=["Workflow Connections"],
)

app.include_router(
    executions_router,
    prefix="/api/v1/executions",
    tags=["Executions"],
)

app.include_router(
    execution_logs_router,
    prefix="/api/v1/execution-logs",
    tags=["Execution Logs"],
)

app.include_router(
    dashboard_router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"],
)

app.include_router(
    schedules_router,
    prefix="/api/v1/schedules",
    tags=["Workflow Scheduler"],
)

app.include_router(
    webhooks_router,
    prefix="/api/v1/webhooks",
    tags=["Webhooks"],
)

app.include_router(
    workflow_templates_router,
    prefix="/api/v1",
    tags=["Workflow Templates"],
)

# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Workflow Automation Platform",
        "status": "running",
        "version": "2.3.0",
    }