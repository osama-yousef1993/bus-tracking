from sqlalchemy import Table, Column, Text, Integer, DateTime, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import UUID
from src.database.execution import db_client
# REMEMEBERRR handle sql injection

status_enum = Enum(
    "active",
    "disabled",
    "in_progress",
    "arrived",
    "under_maintenance",
    "delayed",
    name="status",
)


routes = Table(
    "routes",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("name", Text),
    Column("description", Text),
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

stops = Table(
    "stops",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("route_id", UUID(as_uuid=True), ForeignKey("routes.id")),
    Column("name", Text),
    Column("latitude", Float),
    Column("longitude", Float),
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

buses = Table(
    "buses",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("bus_number", Integer, unique=True),
    Column("start_time", DateTime),
    Column("end_time", DateTime),
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

trips = Table(
    "trips",
    db_client.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=db_client.new_uuid),
    Column("route_id", UUID(as_uuid=True), ForeignKey("routes.id")),
    Column("driver_id", UUID(as_uuid=True), ForeignKey("driver.id")),
    Column("bus_id", UUID(as_uuid=True), ForeignKey("buses.id")),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("status", status_enum),
    Column("current_time", DateTime, **db_client.default_now),
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
