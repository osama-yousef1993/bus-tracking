from enum import Enum
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class StatusEnum(str, Enum):
    active = "active"
    disabled = "disabled"
    in_progress = "in_progress"
    arrived = "arrived"
    under_maintenance = "under_maintenance"
    delayed = "delayed"


class Roles(BaseModel):
    id: UUID
    name: str
    alias: Optional[str] = None
    duties: Optional[dict[str, any]] = None
    description: str
    created_at: datetime
    updated_at: datetime | None = None


class RoleWithPermissions(BaseModel):
    id: UUID
    name: str
    alias: str | None = None
    permissions: list[str] = []


class AdminRoles(BaseModel):
    role_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime | None = None


class RoleRequest(BaseModel):
    name: str
    alias: str | None = None
    duties: Optional[dict[str, any]] = None
    description: str


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None
    duties: Optional[dict[str, any]] = None
    description: Optional[str] = None


class Permission(BaseModel):
    id: UUID
    name: str
    slug: str


class PermissionUpdate(BaseModel):
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class PermissionRequest(BaseModel):
    role: RoleRequest
    permissions: list[Permission]

    class config:
        from_attributes = True


class RolePermission(BaseModel):
    role: Roles
    permissions: list[Permission]

    class config:
        from_attributes = True


class PermissionRole(BaseModel):
    permission: Permission
    roles: list[Roles]

    class config:
        from_attributes = True


class RolePermissionRequest(BaseModel):
    resource_id: str
    assigned_at: datetime


class RolesResponse(BaseModel):
    resource_id: str
    assigned_at: datetime


class UserResponse(BaseModel):
    resource_id: str
    assigned_at: datetime


class UserRoles(BaseModel):
    user: UserResponse
    roles: list[RolesResponse] = []


class RolesUsers(BaseModel):
    role: Roles
    users: list[UserResponse] = []


class UserRoleResponse(BaseModel):
    admin_id: str
    role_id: str
    resource_id: str
    assigned_at: datetime


class AdminRoleResponse(BaseModel):
    admin_id: str
    role_id: str


class UserRoleUpdate(BaseModel):
    admin_id: str
    role_id: str
