from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.app.models.execution import Execution


def create_execution(
    db: Session,
    workflow_id: int,
    input_data: dict | None = None,
) -> Execution:
    execution = Execution(
        workflow_id=workflow_id,
        status="pending",
        input_data=input_data,
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return execution


def get_execution(db: Session, execution_id: int) -> Execution | None:
    return db.query(Execution).filter(Execution.id == execution_id).first()


def get_workflow_executions(db: Session, workflow_id: int) -> list[Execution]:
    return (
        db.query(Execution)
        .filter(Execution.workflow_id == workflow_id)
        .order_by(Execution.created_at.desc())
        .all()
    )


def update_execution_status(
    db: Session,
    execution: Execution,
    status: str,
    output_data: dict | None = None,
    error_message: str | None = None,
):
    now = datetime.now(timezone.utc)
    execution.status = status

    if status == "running" and execution.started_at is None:
        execution.started_at = now

    if status in {"completed", "failed"}:
        execution.finished_at = now

    if output_data is not None:
        execution.output_data = output_data

    if error_message is not None:
        execution.error_message = error_message

    db.commit()
    db.refresh(execution)
    return execution


def delete_execution(db: Session, execution: Execution):
    db.delete(execution)
    db.commit()
