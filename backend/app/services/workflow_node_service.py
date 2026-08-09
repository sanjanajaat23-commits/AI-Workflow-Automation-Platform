from sqlalchemy.orm import Session
from backend.app.models.workflow import Workflow

from backend.app.crud.workflow_node import (
    create_workflow_node,
    delete_workflow_node,
    get_workflow_node,
    get_workflow_nodes,
    update_workflow_node,
)


def create_node(
    db: Session,
    workflow_id: int,
    node_data: dict,
):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise ValueError("Workflow not found.")

    return create_workflow_node(
        db,
        workflow_id,
        node_data,
    )


def list_nodes(
    db: Session,
    workflow_id: int,
):
    return get_workflow_nodes(
        db,
        workflow_id,
    )


def update_node(
    db: Session,
    node_id: int,
    node_data: dict,
):
    node = get_workflow_node(
        db,
        node_id,
    )

    if node is None:
        raise ValueError("Node not found.")

    return update_workflow_node(
        db,
        node,
        node_data,
    )


def remove_node(
    db: Session,
    node_id: int,
):
    node = get_workflow_node(
        db,
        node_id,
    )

    if node is None:
        raise ValueError("Node not found.")

    delete_workflow_node(
        db,
        node,
    )

    return True