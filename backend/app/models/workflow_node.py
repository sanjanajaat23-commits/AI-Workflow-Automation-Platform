from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.database import Base


class WorkflowNode(Base):
    __tablename__ = "workflow_nodes"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    node_key = Column(String(255), nullable=False)
    node_type = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)

    config = Column(JSON, default=dict, nullable=False)

    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)

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

    workflow = relationship(
        "Workflow",
        back_populates="nodes",
    )
