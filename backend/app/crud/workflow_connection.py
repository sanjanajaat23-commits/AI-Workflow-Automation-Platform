from sqlalchemy.orm import Session

from backend.app.models.workflow_connection import WorkflowConnection


def create_connection(
    db: Session,
    workflow_id: int,
    connection_data: dict,
):
    connection = WorkflowConnection(
        workflow_id=workflow_id,
        source_node_key=connection_data["source"],
        target_node_key=connection_data["target"],
        source_handle=connection_data.get("sourceHandle"),
        target_handle=connection_data.get("targetHandle"),
    )

    db.add(connection)
    db.commit()
    db.refresh(connection)

    return connection


def get_connections(
    db: Session,
    workflow_id: int,
):
    return (
        db.query(WorkflowConnection)
        .filter(WorkflowConnection.workflow_id == workflow_id)
        .all()
    )


def delete_connections(
    db: Session,
    workflow_id: int,
):
    (
        db.query(WorkflowConnection)
        .filter(WorkflowConnection.workflow_id == workflow_id)
        .delete()
    )

    db.commit()