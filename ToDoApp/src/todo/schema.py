from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    time: datetime
    email: str

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id:int
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str
    description: str
    time: datetime
    email: str
    class Config:
        from_attributes = True