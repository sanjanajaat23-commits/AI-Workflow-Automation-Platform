from sqlalchemy.orm import Session

from backend.app.crud.workflow import (
    create_workflow,
    delete_workflow,
    get_workflow,
    get_workflows_by_user,
    update_workflow,
)
from backend.app.schemas.workflow import WorkflowCreate, WorkflowUpdate


class WorkflowNotFoundError(Exception):
    pass


class WorkflowPermissionError(Exception):
    pass


def create_new_workflow(db: Session, workflow: WorkflowCreate, user_id: int):
    return create_workflow(db, workflow, user_id)


def list_user_workflows(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return get_workflows_by_user(db, user_id, skip, limit)


def get_owned_workflow(db: Session, workflow_id: int, user_id: int):
    db_workflow = get_workflow(db, workflow_id)

    if db_workflow is None:
        raise WorkflowNotFoundError("Workflow not found.")

    if db_workflow.user_id != user_id:
        raise WorkflowPermissionError("You do not have access to this workflow.")

    return db_workflow


def update_owned_workflow(
    db: Session,
    workflow_id: int,
    user_id: int,
    workflow_update: WorkflowUpdate,
):
    db_workflow = get_owned_workflow(db, workflow_id, user_id)
    return update_workflow(db, db_workflow, workflow_update)


def delete_owned_workflow(db: Session, workflow_id: int, user_id: int):
    db_workflow = get_owned_workflow(db, workflow_id, user_id)
    delete_workflow(db, db_workflow)
