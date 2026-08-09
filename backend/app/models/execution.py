from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.database import Base


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status = Column(
        String(50),
        default="pending",
        nullable=False,
    )

    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    workflow = relationship(
        "Workflow",
        back_populates="executions",
    )

    logs = relationship(
        "ExecutionLog",
        back_populates="execution",
        cascade="all, delete-orphan",
    )
