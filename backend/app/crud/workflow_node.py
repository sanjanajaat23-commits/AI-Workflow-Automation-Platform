from sqlalchemy.orm import Session

from backend.app.models.workflow_node import WorkflowNode


def create_workflow_node(
    db: Session,
    workflow_id: int,
    node_data: dict,
):
    node = WorkflowNode(
        workflow_id=workflow_id,
        node_key=node_data["node_key"],
        node_type=node_data["node_type"],
        name=node_data["name"],
        config=node_data.get("config", {}),
        position_x=node_data.get("position_x", 0),
        position_y=node_data.get("position_y", 0),
    )

    db.add(node)
    db.commit()
    db.refresh(node)

    return node


def get_workflow_nodes(
    db: Session,
    workflow_id: int,
):
    return (
        db.query(WorkflowNode)
        .filter(WorkflowNode.workflow_id == workflow_id)
        .all()
    )


def get_workflow_node(
    db: Session,
    node_id: int,
):
    return (
        db.query(WorkflowNode)
        .filter(WorkflowNode.id == node_id)
        .first()
    )


def update_workflow_node(
    db: Session,
    node: WorkflowNode,
    node_data: dict,
):
    node.name = node_data.get("name", node.name)
    node.config = node_data.get("config", node.config)
    node.position_x = node_data.get("position_x", node.position_x)
    node.position_y = node_data.get("position_y", node.position_y)

    db.commit()
    db.refresh(node)

    return node


def delete_workflow_node(
    db: Session,
    node: WorkflowNode,
):
    db.delete(node)
    db.commit()