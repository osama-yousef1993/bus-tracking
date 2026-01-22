from sqlalchemy import Table, Column, Text, Integer, DateTime, Boolean, ForeignKey, Enum
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

driver = Table(
    "driver",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("admin_id", UUID(as_uuid=True), ForeignKey("admin.id")),
    Column("name", Text),
    Column("email", Text, unique=True),
    Column("password", Text),
    Column("bus_number", Integer),
    Column("phone", Text),
    Column("is_deleted", Boolean, default=False),
    Column("is_active", Boolean, default=True),
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
