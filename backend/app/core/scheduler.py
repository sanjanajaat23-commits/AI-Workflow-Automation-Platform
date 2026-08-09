from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from backend.app.services.scheduler_service import scheduler

background_scheduler = BackgroundScheduler()


def start_scheduler():
    if background_scheduler.running:
        return

    background_scheduler.add_job(
        func=scheduler.run_pending,
        trigger=IntervalTrigger(minutes=1),
        id="workflow_scheduler",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    background_scheduler.start()

    print("=" * 60)
    print("Workflow Scheduler Started")
    print("Running every 1 minute")
    print("=" * 60)


def stop_scheduler():
    if background_scheduler.running:
        background_scheduler.shutdown(wait=False)