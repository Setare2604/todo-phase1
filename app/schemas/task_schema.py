from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal

StatusEnum = Literal["todo", "doing", "done"]

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=150)
    deadline: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=150)
    deadline: Optional[datetime] = None
    status: Optional[StatusEnum] = None

class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: StatusEnum
    deadline: Optional[datetime]
    closed_at: Optional[datetime]

    class Config:
        from_attributes = True