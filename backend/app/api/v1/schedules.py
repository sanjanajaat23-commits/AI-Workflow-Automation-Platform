from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.schedule import WorkflowSchedule
from backend.app.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
)

router = APIRouter()


# --------------------------------------------------
# Create Schedule
# --------------------------------------------------

@router.post(
    "",
    response_model=ScheduleResponse,
)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
):
    new_schedule = WorkflowSchedule(
        workflow_id=schedule.workflow_id,
        cron=schedule.cron,
        enabled=True,
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return new_schedule


# --------------------------------------------------
# List Schedules
# --------------------------------------------------

@router.get(
    "",
    response_model=list[ScheduleResponse],
)
def get_schedules(
    db: Session = Depends(get_db),
):
    return (
        db.query(WorkflowSchedule)
        .order_by(WorkflowSchedule.id.desc())
        .all()
    )


# --------------------------------------------------
# Get One Schedule
# --------------------------------------------------

@router.get(
    "/{schedule_id}",
    response_model=ScheduleResponse,
)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    schedule = (
        db.query(WorkflowSchedule)
        .filter(
            WorkflowSchedule.id == schedule_id
        )
        .first()
    )

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found.",
        )

    return schedule


# --------------------------------------------------
# Enable / Disable Schedule
# --------------------------------------------------

@router.put(
    "/{schedule_id}/toggle",
    response_model=ScheduleResponse,
)
def toggle_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    schedule = (
        db.query(WorkflowSchedule)
        .filter(
            WorkflowSchedule.id == schedule_id
        )
        .first()
    )

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found.",
        )

    schedule.enabled = not schedule.enabled

    db.commit()
    db.refresh(schedule)

    return schedule


# --------------------------------------------------
# Delete Schedule
# --------------------------------------------------

@router.delete(
    "/{schedule_id}"
)
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    schedule = (
        db.query(WorkflowSchedule)
        .filter(
            WorkflowSchedule.id == schedule_id
        )
        .first()
    )

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found.",
        )

    db.delete(schedule)
    db.commit()

    return {
        "message": "Schedule deleted successfully."
    }