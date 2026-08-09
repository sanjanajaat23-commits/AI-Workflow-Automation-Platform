from sqlalchemy.orm import Session
from backend.app.models.workflow import Workflow

from backend.app.crud.workflow_connection import (
    create_connection,
    get_connections,
    delete_connections,
)


def save_connections(
    db: Session,
    workflow_id: int,
    connections: list,
):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise ValueError("Workflow not found.")

    # Remove old connections
    delete_connections(
        db=db,
        workflow_id=workflow_id,
    )

    saved_connections = []

    for connection in connections:
        saved_connections.append(
            create_connection(
                db=db,
                workflow_id=workflow_id,
                connection_data=connection,
            )
        )

    return saved_connections


def list_connections(
    db: Session,
    workflow_id: int,
):
    return get_connections(
        db=db,
        workflow_id=workflow_id,
    )