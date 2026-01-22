from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from src.authentication.auth_dependencies.auth_dependencies import CurrentUser
from src.authorization.models import Roles
from src.authorization.services import AuthorizationServices
from src.helpers.common_models import RequestData


router = APIRouter(prefix="/api/v1/admin", tags=["Admin: Authorization"])

services_auth = AuthorizationServices()


@router.get(
    "/roles",
    response_model=Roles,
    description="""
   Retrieve all roles from the database.


   This endpoint:
   - Fetches all role records
   - Requires admin-level authentication
   - Returns paginated list of roles


   Parameters:
   - Valid JWT token in Authorization header


   Returns:
   - 200: Success with roles list
   - 401: Unauthorized if invalid/missing token
   - 403: Forbidden if insufficient permissions
   - 500: Internal server error
   """,
    responses={
        200: {"description": "Successfully retrieved all roles"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - insufficient permissions"},
        500: {"description": "Internal server error"},
    },
    summary="Get all roles",
)
async def get_roles(
    request_data: RequestData = Depends(CurrentUser(user_type="admin")),
) -> JSONResponse:
    content = services_auth.get_roles(request_data)
    return JSONResponse(content=content)


# @router.post(
#     "/add_role_permission",
#     response_model=RolePermissionRequest,
#     description="""
#     Retrieve all roles from the database.


#     This endpoint:
#     - Fetches all role records
#     - Requires admin-level authentication
#     - Returns paginated list of roles


#     Parameters:
#     - Valid JWT token in Authorization header


#     Returns:
#     - 200: Success with roles list
#     - 401: Unauthorized if invalid/missing token
#     - 403: Forbidden if insufficient permissions
#     - 500: Internal server error
#     """,
#     responses={
#         200: {"description": "Successfully retrieved all roles"},
#         401: {"description": "Unauthorized - invalid or missing token"},
#         403: {"description": "Forbidden - insufficient permissions"},
#         500: {"description": "Internal server error"},
#     },
#     summary="Get all roles",
# )
# async def insert_roles(data: RolePermissionRequest) -> JSONResponse:
#     content, status_code = services_auth.insert_role_permissions(data)
#     return JSONResponse(status_code=status_code, content=content)


# @router.post(
#     "/add_admin_role",
#     response_model=RolePermissionRequest,
#     description="""
#     Retrieve all roles from the database.


#     This endpoint:
#     - Fetches all role records
#     - Requires admin-level authentication
#     - Returns paginated list of roles


#     Parameters:
#     - Valid JWT token in Authorization header


#     Returns:
#     - 200: Success with roles list
#     - 401: Unauthorized if invalid/missing token
#     - 403: Forbidden if insufficient permissions
#     - 500: Internal server error
#     """,
#     responses={
#         200: {"description": "Successfully retrieved all roles"},
#         401: {"description": "Unauthorized - invalid or missing token"},
#         403: {"description": "Forbidden - insufficient permissions"},
#         500: {"description": "Internal server error"},
#     },
#     summary="Get all roles",
# )
# async def insert_admin_roles(data: AdminRoleRequest) -> JSONResponse:
#     content, status_code = services_auth.insert_admin_role(data)
#     return JSONResponse(status_code=status_code, content=content)
