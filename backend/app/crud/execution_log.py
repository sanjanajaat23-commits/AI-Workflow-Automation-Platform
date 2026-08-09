from sqlalchemy.orm import Session

from backend.app.models.execution_log import ExecutionLog


def create_log(
    db: Session,
    execution_id: int,
    message: str,
    level: str = "info",
) -> ExecutionLog:
    log = ExecutionLog(
        execution_id=execution_id,
        message=message,
        level=level,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_execution_logs(
    db: Session,
    execution_id: int,
) -> list[ExecutionLog]:
    return (
        db.query(ExecutionLog)
        .filter(ExecutionLog.execution_id == execution_id)
        .order_by(ExecutionLog.created_at.asc())
        .all()
    )
