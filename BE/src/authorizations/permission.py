from uuid import UUID


from sqlalchemy import select


from src.authorization.schemas import permissions
from src.database.client import db_client


class PermissionQueries:
    def __init__(self):
        self.db_client = db_client

    def get_permissions(self):
        query = select(permissions).group_by(permissions.c.category)
        rows = self.db_client.execute_all(query)
        return rows

    def get_permissions_by_id(self, permission_id: UUID):
        query = permissions.select().where(permissions.c.id == permission_id)
        row = self.db_client.execute_one(query)
        return row

    def get_permission_by_slug(self, slug: str):
        query = permissions.select().where(permissions.c.slug == slug)
        row = self.db_client.execute_one(query)
        return row
