# пайдентик схемы для запросов и ответов

from pathlib import Path
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Union, Optional


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None

class TaskCreate(TaskBase):
    # completed: bool = False
    pass

class TaskUpdate(TaskBase):
    # completed: bool
    pass

class TaskUpdated(BaseModel):
    completed: bool

class TaskResponse(TaskBase):
    id: int
    completed: bool
    owner_id: int

    class config:
        orm_mode = True

class UserShema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    username: str
    password: bytes
    email: Union[EmailStr, None] = None
    active: bool = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: Union[EmailStr, None] = None


