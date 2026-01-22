from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class StudentCreate(BaseModel):
    student_id: UUID
    name: str
    email: str
    major: Optional[str] = None
    created_at: datetime = datetime.now()


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    major: Optional[str] = None
    updated_at: Optional[datetime] = None


class StudentDelete(BaseModel):
    deleted_at: datetime = datetime.now()
