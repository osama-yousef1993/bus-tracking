from uuid import UUID


from sqlalchemy import func, select


from src.admins.schemas import admins
from src.authorization.models import AdminRoleRequest, RolePermissionRequest
from src.authorization.schemas import admin_role, permissions, role_permissions, roles
from src.database.client import db_client


class RoleQueries:
    def __init__(self):
        self.db_client = db_client
        self.join_table = roles.outerjoin(
            role_permissions, roles.c.id == role_permissions.c.role_id
        ).outerjoin(permissions, role_permissions.c.permission_id == permissions.c.id)
        self.admin_role_join_table = (
            admins.outerjoin(admin_role, admins.c.id == admin_role.c.admin_id)
            .outerjoin(roles, admin_role.c.role_id == roles.c.id)
            .outerjoin(role_permissions, roles.c.id == role_permissions.c.role_id)
            .outerjoin(
                permissions, role_permissions.c.permission_id == permissions.c.id
            )
        )

    def get_roles(self):
        query = roles.select()
        rows = self.db_client.execute_all(query)
        return rows

    def get_admin_role_permissions(self, admin_id: UUID):
        query = (
            select(
                admins,
                func.jsonb_agg(
                    func.jsonb_build_object(
                        "id", roles.c.id, "name", roles.c.name, "alias", roles.c.alias
                    )
                )
                .op("->")(0)
                .label("roles"),
                func.array_agg(func.distinct(permissions.c.slug))
                .filter(permissions.c.id.isnot(None))
                .label("permissions"),
            )
            .select_from(self.admin_role_join_table)
            .where(admins.c.id == admin_id)
            .group_by(admins.c.id)
        )

        row = self.db_client.execute_one(query)
        if not row:
            return None
        return row

    def get_role_by_id(self, role_id: UUID):
        # Build query to join roles with permissions through role_permissions
        query = (
            select(
                roles.c.id,
                roles.c.name,
                roles.c.alias,
                func.array_agg(permissions.c.slug).label("permissions"),
            )
            .select_from(self.join_table)
            .where(roles.c.id == role_id)
            .group_by(roles.c.id, roles.c.name, roles.c.alias)
        )

        row = self.db_client.execute_one(query)
        if not row:
            return None

        # Map to your desired JSON-like structure
        return {
            "id": row["id"],
            "name": row["name"],
            "alias": row["alias"],
            "permissions": row["permissions"] or [],
        }

    def get_role_by_name(self, role_name: str):
        # Build query to join roles with permissions through role_permissions
        query = (
            select(
                roles.c.id,
                roles.c.name.label("role_name"),
                roles.c.alias,
                func.array_agg(permissions.c.slug).label("permissions"),
            )
            .select_from(self.join_table)
            .where(roles.c.name == role_name)
            .group_by(roles.c.id, roles.c.name, roles.c.alias)
        )

        row = self.db_client.execute_one(query)
        if not row:
            return None

        # Map to your desired JSON-like structure
        return {
            "id": row.id,
            "name": row.role_name,
            "alias": row.alias,
            "permissions": row.permissions or [],
        }

    def insert_role_permission(self, role_data: RolePermissionRequest):
        query = (
            role_permissions.insert()
            .values(dict(role_data))
            .returning(role_permissions)
        )
        row = self.db_client.execute_one(query)
        return row

    def insert_admin_role(self, admin_role_data: AdminRoleRequest):
        query = admin_role.insert().values(dict(admin_role_data)).returning(admin_role)
        row = self.db_client.execute_one(query)
        return row

    def delete_admin_role(self, id: UUID):
        query = admin_role.delete().where(admin_role.c.id == id).returning(admin_role)
        rows = self.db_client.execute_one(query)
        return rows
