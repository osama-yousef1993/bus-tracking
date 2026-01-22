from sqlalchemy import create_engine, MetaData
import uuid
from datetime import datetime, timezone
from typing import Any
from src.utils.config import get_database_url
from sqlalchemy import func


engine = create_engine(get_database_url())
metadata = MetaData()
metadata.create_all(bind=engine)

new_uuid = uuid.uuid4
now = datetime.now(timezone.utc)
default_now: dict[str, Any] = {"default": now, "server_default": func.now()}
