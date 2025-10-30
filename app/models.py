from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    task: str = Field(..., min_length=3)


class RunResponse(BaseModel):
    task: str
    plan: str
    technician_notes: str
    safety_review: str
    sources: list[str] = Field(default_factory=list)
    mode: str
