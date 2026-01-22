from sqlalchemy import Double, Enum, ForeignKey, Table, Column, Text, DateTime
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

stops = Table(
    "stops",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("route_id", UUID(as_uuid=True), ForeignKey("routes.id")),
    Column("name", Text),
    Column("latitude", Double),
    Column("longitude", Double),
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
