from src.database.connection import engine, metadata, new_uuid, now, default_now
from sqlalchemy.exc import IntegrityError, OperationalError
from flask import abort


class DBClient:
    def __init__(self):
        self.engine = engine
        self.metadata = metadata
        self.new_uuid = new_uuid
        self.now = now
        self.default_now = default_now

    def execute_all(self, query):
        try:
            with self.engine.begin() as conn:
                result = conn.execute(query)

                rows = result.mappings().all()
                if not rows:
                    return False
                return [dict(row) for row in rows]

        except IntegrityError as e:
            detail = f"Database integrity constraint violated: {str(e)}."
            abort(409, description=detail)
        except OperationalError as e:
            detail = f"Unexpected database error: {str(e)}"
            abort(500, description=detail)
        except Exception as e:
            detail = f"Unexpected error: {str(e)}"
            abort(500, description=detail)

    def execute_one(self, query):
        try:
            with self.engine.begin() as conn:
                result = conn.execute(query)

                row = result.mappings().first()
                if not row:
                    return None
                return dict(row)

        except IntegrityError as e:
            detail = f"Database integrity constraint violated: {str(e)}."
            abort(409, description=detail)
        except OperationalError as e:
            detail = f"Unexpected database error: {str(e)}"
            abort(500, description=detail)
        except Exception as e:
            detail = f"Unexpected error: {str(e)}"
            abort(500, description=detail)


db_client = DBClient()
