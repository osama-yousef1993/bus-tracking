from fastapi import APIRouter, Depends
from src.drivers.query import DriverQueries
from src.drivers.model import DriverCreate
from src.drivers.service import DriverService
from uuid import UUID
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/drivers", tags=["Drivers"])


def get_driver_service():
    return DriverService(DriverQueries())


@router.post("/", response_model=dict)
async def register_driver(
    payload: DriverCreate,
    service: DriverService = Depends(get_driver_service),
):
    status_code, driver_data = await service.create_user(payload)
    return JSONResponse(content=driver_data, status_code=status_code)


@router.get("/{driver_id}", response_model=dict)
async def get_driver(
    driver_id: UUID,
    service: DriverService = Depends(get_driver_service),
):
    driver = await service.get_driver_by_id(driver_id)
    if not driver:
        return JSONResponse(content={"detail": "Driver not found"}, status_code=404)
    return driver
