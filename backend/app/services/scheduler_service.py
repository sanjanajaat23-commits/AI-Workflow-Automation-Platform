from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.schedule import WorkflowSchedule
from backend.app.models.workflow import Workflow
from backend.app.services.workflow_executor import WorkflowExecutor


class SchedulerService:

    def run_pending(self):
        db: Session = SessionLocal()

        try:
            schedules = (
                db.query(WorkflowSchedule)
                .filter(
                    WorkflowSchedule.enabled.is_(True)
                )
                .all()
            )

            if not schedules:
                return

            for schedule in schedules:

                workflow = (
                    db.query(Workflow)
                    .filter(
                        Workflow.id == schedule.workflow_id
                    )
                    .first()
                )

                if workflow is None:
                    continue

                if not workflow.is_active:
                    continue

                try:
                    WorkflowExecutor(db).execute(workflow)

                    print(
                        f"[Scheduler] Executed workflow {workflow.id}"
                    )

                except Exception as e:
                    print(
                        f"[Scheduler] Workflow {workflow.id} failed: {e}"
                    )

        finally:
            db.close()


scheduler = SchedulerService()