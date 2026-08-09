from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.services.workflow_node_service import (
    create_node,
    list_nodes,
    update_node,
    remove_node,
)

router = APIRouter()


@router.post("/{workflow_id}/nodes")
def create_workflow_node(
    workflow_id: int,
    node_data: dict,
    db: Session = Depends(get_db),
):
    try:
        return create_node(
            db=db,
            workflow_id=workflow_id,
            node_data=node_data,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{workflow_id}/nodes")
def get_workflow_nodes(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    return list_nodes(
        db=db,
        workflow_id=workflow_id,
    )


@router.put("/nodes/{node_id}")
def update_workflow_node(
    node_id: int,
    node_data: dict,
    db: Session = Depends(get_db),
):
    try:
        return update_node(
            db=db,
            node_id=node_id,
            node_data=node_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete("/nodes/{node_id}")
def delete_workflow_node(
    node_id: int,
    db: Session = Depends(get_db),
):
    try:
        remove_node(
            db=db,
            node_id=node_id,
        )

        return {
            "message": "Node deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )