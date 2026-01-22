from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from manjam_common.helpers.custom_response import CustomResponse
from manjam_common.helpers.random import RandomHelper


from src.admins.queries.admins import AdminQueries
from src.authorization.models import (
    AdminRoleRequest,
    RolePermissionRequest,
    Roles,
    RoleWithPermissionResponse,
)
from src.authorization.queries.permissions import PermissionQueries
from src.authorization.queries.roles import RoleQueries
from src.helpers.check_instance import InstanceServices
from src.helpers.check_permission import CheckPermission
from src.helpers.common_models import RequestData


class AuthorizationServices:
    def __init__(
        self,
    ):
        self.admin_queries = AdminQueries()
        self.roles_queries = RoleQueries()
        self.permission_queries = PermissionQueries()
        self.instance_services = InstanceServices()
        self.check_permission = CheckPermission()
        self.custom_response = CustomResponse()
        self.random_helper = RandomHelper()

    def get_role_permissions_admin_id(
        self, admin_id: int
    ) -> RoleWithPermissionResponse:
        row = self.roles_queries.get_admin_role_permissions(admin_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Roles Found for the admin.",
            )
        content = RoleWithPermissionResponse(
            **row["roles"],
            permissions=row["permissions"],
        )
        return jsonable_encoder(content)

    def get_roles(self, request_data: RequestData):
        try:
            admin_token = self.instance_services.require_admin_token(request_data)
            self.admin_id = admin_token.admin_id
            self.check_permission.check_admin_access(self.admin_id, ["view_roles"])
            admin = self.admin_queries.get_admin_by_id(self.admin_id)
            if not admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or missing admin token.",
                )

            roles: list[Roles] = []
            role_rows = self.roles_queries.get_roles()

            if not role_rows:
                response = self.custom_response.build_response(
                    content=jsonable_encoder(roles),
                    status_code=status.HTTP_204_NO_CONTENT,
                    message="No Roles Found.",
                    request_id=f"roles_{self.random_helper.random_int(1000, 10000)}",
                )
                return jsonable_encoder(response)

            for role in role_rows:
                roles.append(Roles(**role))

            response = self.custom_response.build_response(
                content=jsonable_encoder(roles),
                status_code=status.HTTP_200_OK,
                message="Roles retrieved successfully.",
                request_id=f"roles_{self.random_helper.random_int(1000, 10000)}",
            )
            return jsonable_encoder(response)

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve roles",
            )

    def insert_role_permissions(self, role_data: RolePermissionRequest):
        try:
            row = self.role_permission_queries.insert_role_permission(role_data)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Failed to Create Roles Permission. Possible reasons: invalid data or database error.",
                )
            role = dict(row)
            response = self.custom_response.build_response(
                content=jsonable_encoder(RolePermissionRequest(**dict(role))),
                status_code=status.HTTP_201_CREATED,
                message="Roles Inserted successfully.",
                request_id=f"create_roles_{self.random_helper.random_int(1000, 10000)}",
            )
            return jsonable_encoder(response)

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to Add new Roles Permission",
            )

    def insert_admin_role(self, role_data: AdminRoleRequest):
        try:
            row = self.role_permission_queries.insert_admin_role(role_data)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Failed to Create Roles Permission. Possible reasons: invalid data or database error.",
                )
            role = dict(row)
            response = self.custom_response.build_response(
                content=jsonable_encoder(AdminRoleRequest(**dict(role))),
                status_code=status.HTTP_201_CREATED,
                message="Roles Inserted successfully.",
                request_id=f"create_roles_{self.random_helper.random_int(1000, 10000)}",
            )
            return jsonable_encoder(response)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to Add new Roles Permission",
            )
