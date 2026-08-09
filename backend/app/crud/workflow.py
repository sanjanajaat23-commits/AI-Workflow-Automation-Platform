from sqlalchemy.orm import Session

from backend.app.models.workflow import Workflow
from backend.app.schemas.workflow import WorkflowCreate, WorkflowUpdate


def create_workflow(db: Session, workflow: WorkflowCreate, user_id: int) -> Workflow:
    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        is_active=workflow.is_active,
        user_id=user_id,
    )

    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)

    return db_workflow


def get_workflow(db: Session, workflow_id: int) -> Workflow | None:
    return db.query(Workflow).filter(Workflow.id == workflow_id).first()


def get_workflows_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Workflow]:
    return (
        db.query(Workflow)
        .filter(Workflow.user_id == user_id)
        .order_by(Workflow.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_workflow(
    db: Session,
    db_workflow: Workflow,
    workflow_update: WorkflowUpdate,
) -> Workflow:
    update_data = workflow_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_workflow, field, value)

    db.commit()
    db.refresh(db_workflow)

    return db_workflow


def delete_workflow(db: Session, db_workflow: Workflow) -> None:
    db.delete(db_workflow)
    db.commit()
