from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi_pagination import Params as BaseParam

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

class PaginatedTaskResponse(BaseModel):
    tasks: List[TaskResponse]
    total_count: int
    page: int
    page_size: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserID(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
