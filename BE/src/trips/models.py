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


class TripCreate(BaseModel):
    id: UUID
    route_id: UUID
    driver_id: UUID
    bus_id: UUID
    latitude: float
    longitude: float
    status: StatusEnum
    current_time: datetime = datetime.now()
    created_at: datetime = datetime.now()


class TripUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[StatusEnum] = None
    current_time: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TripDelete(BaseModel):
    deleted_at: Optional[datetime] = None
