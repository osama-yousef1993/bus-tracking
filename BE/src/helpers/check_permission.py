from typing import List
from uuid import UUID


from fastapi import HTTPException, status


from src.authorization.queries.roles import RoleQueries


class CheckPermission:
    def __init__(self):
        self.roles_queries = RoleQueries()

    def check_admin_access(self, admin_id: UUID, function_perme: List[str]):
        admin_role_permissions = self.roles_queries.get_admin_role_permissions(admin_id)
        if not admin_role_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You don't have any permission to make this request.",
            )

        for perm in function_perme:
            if perm in admin_role_permissions["permissions"]:
                return True
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You don't have any permission to make this request.",
            )
