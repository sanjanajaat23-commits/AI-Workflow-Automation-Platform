from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.services.execution_log_service import (
    ExecutionNotFoundError,
    list_logs,
)

router = APIRouter()


@router.get(
    "/{execution_id}",
    tags=["Execution Logs"],
)
def get_execution_logs(
    execution_id: int,
    db: Session = Depends(get_db),
):
    try:
        return list_logs(
            db=db,
            execution_id=execution_id,
        )

    except ExecutionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
