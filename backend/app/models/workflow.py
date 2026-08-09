from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.database import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ---------------------------------------
    # Relationships
    # ---------------------------------------

    owner = relationship(
        "User",
        back_populates="workflows",
    )

    nodes = relationship(
        "WorkflowNode",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )

    connections = relationship(
        "WorkflowConnection",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )

    executions = relationship(
        "Execution",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )

    schedules = relationship(
        "WorkflowSchedule",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )