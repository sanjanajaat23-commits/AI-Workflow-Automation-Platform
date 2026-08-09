from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from backend.app.database.database import Base


class WorkflowSchedule(Base):
    __tablename__ = "workflow_schedules"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    workflow_id = Column(
        Integer,
        ForeignKey(
            "workflows.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    cron = Column(
        String(100),
        nullable=False,
    )

    enabled = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    workflow = relationship(
        "Workflow",
        back_populates="schedules",
    )