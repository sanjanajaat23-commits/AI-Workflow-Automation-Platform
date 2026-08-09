from sqlalchemy.orm import Session

from backend.app.crud.execution import get_execution
from backend.app.crud.execution_log import (
    create_log,
    get_execution_logs,
)


class ExecutionNotFoundError(Exception):
    pass


def add_log(
    db: Session,
    execution_id: int,
    message: str,
    level: str = "info",
):
    execution = get_execution(db, execution_id)

    if execution is None:
        raise ExecutionNotFoundError("Execution not found.")

    return create_log(
        db=db,
        execution_id=execution_id,
        message=message,
        level=level,
    )


def list_logs(
    db: Session,
    execution_id: int,
):
    execution = get_execution(db, execution_id)

    if execution is None:
        raise ExecutionNotFoundError("Execution not found.")

    return get_execution_logs(
        db,
        execution_id,
    )
