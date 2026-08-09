from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = False


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
