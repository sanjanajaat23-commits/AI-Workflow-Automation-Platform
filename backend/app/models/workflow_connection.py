from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.database import Base


class WorkflowConnection(Base):
    __tablename__ = "workflow_connections"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_node_key = Column(String(255), nullable=False)
    target_node_key = Column(String(255), nullable=False)

    source_handle = Column(String(255), nullable=True)
    target_handle = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    workflow = relationship(
        "Workflow",
        back_populates="connections",
    )
