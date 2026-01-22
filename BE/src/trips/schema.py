from sqlalchemy import Double, Enum, ForeignKey, Table, Column, DateTime
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

trips = Table(
    "trips",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("route_id", UUID(as_uuid=True), ForeignKey("routes.id")),
    Column("driver_id", UUID(as_uuid=True), ForeignKey("driver.id")),
    Column("bus_id", UUID(as_uuid=True), ForeignKey("buses.id")),
    Column("latitude", Double),
    Column("longitude", Double),
    Column("status", status_enum),
    Column("current_time", DateTime, nullable=False, **db_client.default_now),
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
