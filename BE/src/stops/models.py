from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class StatusEnum(str, Enum):
    active = "active"
    disabled = "disabled"
    in_progress = "in_progress"
    arrived = "arrived"
    under_maintenance = "under_maintenance"
    delayed = "delayed"


class RouteCreate(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    status: StatusEnum
    created_at: datetime = datetime.now()


class RouteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    updated_at: Optional[datetime] = None


class RouteDelete(BaseModel):
    deleted_at: Optional[datetime] = None
