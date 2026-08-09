from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    workflow_id: int
    cron: str


class ScheduleResponse(BaseModel):
    id: int
    workflow_id: int
    cron: str
    enabled: bool

    class Config:
        from_attributes = True