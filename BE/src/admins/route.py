from fastapi import APIRouter, Depends
from src.admins.model import AdminCreate, AdminResponse
from src.admins.service import AdminService
from uuid import UUID
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/admins", tags=["Admins"])


def get_admin_service():
    return AdminService()


@router.post("/", response_model=AdminResponse)
async def register_admin(
    payload: AdminCreate,
    service: AdminService = Depends(get_admin_service),
):
    status_code, admin_data = await service.create_user(payload)
    return JSONResponse(content=admin_data, status_code=status_code)


@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin(
    admin_id: UUID,
    service: AdminService = Depends(get_admin_service),
):
    status_code, admin_data = await service.get_admin_by_id(admin_id)
    return JSONResponse(content=admin_data, status_code=status_code)
