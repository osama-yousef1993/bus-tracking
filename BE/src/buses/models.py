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


class BusCreate(BaseModel):
    id: UUID
    bus_number: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: StatusEnum
    created_at: datetime = datetime.now()


class BusUpdate(BaseModel):
    bus_number: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[StatusEnum] = None
    updated_at: Optional[datetime] = None


class BusDelete(BaseModel):
    deleted_at: Optional[datetime] = None
