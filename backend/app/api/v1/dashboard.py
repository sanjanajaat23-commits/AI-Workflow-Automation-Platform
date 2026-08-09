from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.workflow import Workflow
from backend.app.models.execution import Execution

router = APIRouter()


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
):
    workflows = db.query(Workflow).count()

    running = (
        db.query(Execution)
        .filter(Execution.status == "running")
        .count()
    )

    completed = (
        db.query(Execution)
        .filter(Execution.status == "completed")
        .count()
    )

    failed = (
        db.query(Execution)
        .filter(Execution.status == "failed")
        .count()
    )

    return {
        "workflows": workflows,
        "running": running,
        "completed": completed,
        "failed": failed,
    }