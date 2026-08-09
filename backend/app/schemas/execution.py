from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExecutionResponse(BaseModel):
    id: int

    workflow_id: int

    status: str

    input_data: dict | None = None

    output_data: dict | None = None

    error_message: str | None = None

    started_at: datetime | None = None

    finished_at: datetime | None = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )