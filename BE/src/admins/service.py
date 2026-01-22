from src.admins.model import AdminCreate, AdminResponse
from src.admins.query import AdminQueries
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException
from uuid import UUID


class AdminService:
    def __init__(self, queries: AdminQueries):
        self.queries = queries

    async def create_user(self, admin_data: AdminCreate):
        # check admin by email
        existing_admin = self.queries.get_user_by_email(admin_data.email)
        if existing_admin:
            message = {"detail": "Admin already exists"}
            return status.HTTP_409_CONFLICT, jsonable_encoder(message)
        # new admin creation
        try:
            admin = self.queries.create_user(admin_data)
            if not admin:
                message = {"detail": "Could not create admin"}
                return status.HTTP_400_BAD_REQUEST, jsonable_encoder(message)
            admin_data = AdminResponse(**admin)
            return status.HTTP_201_CREATED, jsonable_encoder(admin_data)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Error creating admin: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, None

    async def get_admin_by_id(self, admin_id: UUID):
        admin = self.queries.get_user_by_id(admin_id)
        if not admin:
            return None
        return AdminResponse(**admin)

    async def update_admin(self, admin_id: UUID, update_data: dict):
        try:
            admin = self.queries.update_user(admin_id, update_data)
            if not admin:
                return None
            return AdminResponse(**admin)
        except Exception as e:
            print(f"Error updating admin: {e}")
            return None

    async def delete_admin(self, admin_id: UUID):
        try:
            admin = self.queries.delete(admin_id)
            if not admin:
                return None
            return AdminResponse(**admin)
        except Exception as e:
            print(f"Error deleting admin: {e}")
            return None
