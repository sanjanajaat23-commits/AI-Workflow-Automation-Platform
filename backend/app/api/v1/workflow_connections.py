from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.services.workflow_connection_service import (
    save_connections,
    list_connections,
)

router = APIRouter()


@router.post("/{workflow_id}/connections")
def save_workflow_connections(
    workflow_id: int,
    connections: list[dict[str, Any]] = Body(...),
    db: Session = Depends(get_db),
):
    try:
        return save_connections(
            db=db,
            workflow_id=workflow_id,
            connections=connections,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{workflow_id}/connections")
def get_workflow_connections(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    return list_connections(
        db=db,
        workflow_id=workflow_id,
    )