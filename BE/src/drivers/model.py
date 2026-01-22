from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class DriverCreate(BaseModel):
    id: UUID
    name: str
    email: str
    bus_number: int
    phone: int
    created_at: datetime = datetime.now()


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    bus_number: Optional[int] = None
    phone: Optional[int] = None
    updated_at: Optional[datetime] = None


class Driver(BaseModel):
    id: UUID
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class DriverDelete(Driver):
    deleted_at: Optional[datetime] = None
