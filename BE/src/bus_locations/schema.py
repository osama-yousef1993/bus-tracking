from sqlalchemy import Enum, ForeignKey, Table, Column, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.database.execution import db_client

status_enum = Enum(
    "active",
    "disabled",
    "in_progress",
    "arrived",
    "under_maintenance",
    "delayed",
    name="status",
)

bus_location = Table(
    "bus_location",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("bus_id", UUID(as_uuid=True), ForeignKey("buses.id")),
    Column("trip_id", UUID(as_uuid=True), ForeignKey("trips.id")),
    Column("capacity", Text),
    Column("status", status_enum),
    Column("created_at", DateTime, nullable=False, **db_client.default_now),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        onupdate=db_client.now,
        **db_client.default_now,
    ),
    Column("deleted_at", DateTime, nullable=True),
)
