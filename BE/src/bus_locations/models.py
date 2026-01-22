from enum import Enum
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class StatusEnum(str, Enum):
    active = "active"
    disabled = "disabled"
    in_progress = "in_progress"
    arrived = "arrived"
    under_maintenance = "under_maintenance"
    delayed = "delayed"


class BusLocationCreate(BaseModel):
    id: UUID
    bus_id: UUID
    trip_id: UUID
    capacity: str
    status: StatusEnum
    created_at: datetime = datetime.now()


class BusLocationUpdate(BaseModel):
    capacity: Optional[str] = None
    status: Optional[StatusEnum] = None
    updated_at: Optional[datetime] = None


class BusLocationDelete(BaseModel):
    deleted_at: Optional[datetime] = None
