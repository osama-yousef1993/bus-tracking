from src.drivers.model import DriverCreate
from src.drivers.query import DriverQueries
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException
from uuid import UUID


class DriverService:
    def __init__(self, queries: DriverQueries):
        self.queries = queries

    async def create_user(self, driver_data: DriverCreate):
        existing_driver = self.queries.get_user_by_email(driver_data.email)
        if existing_driver:
            message = {"detail": "Driver already exists"}
            return status.HTTP_409_CONFLICT, jsonable_encoder(message)
        try:
            driver = self.queries.create_user(driver_data)
            if not driver:
                message = {"detail": "Could not create driver"}
                return status.HTTP_400_BAD_REQUEST, jsonable_encoder(message)
            return status.HTTP_201_CREATED, jsonable_encoder(driver)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error creating driver: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, None

    async def get_driver_by_id(self, driver_id: UUID):
        driver = self.queries.get_user_by_id(driver_id)
        if not driver:
            return None
        return driver

    async def update_driver(self, driver_id: UUID, update_data: dict):
        try:
            driver = self.queries.update_user(driver_id, update_data)
            if not driver:
                return None
            return driver
        except Exception as e:
            print(f"Error updating driver: {e}")
            return None

    async def delete_driver(self, driver_id: UUID):
        try:
            driver = self.queries.soft_delete(driver_id)
            if not driver:
                return None
            return driver
        except Exception as e:
            print(f"Error deleting driver: {e}")
            return None
