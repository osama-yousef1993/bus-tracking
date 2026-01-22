from sqlalchemy import select, insert, update, delete, and_
from src.database.schema import driver
from src.authentications.hash import HashHelper
from src.database.execution import db_client
from src.drivers.model import DriverCreate
from uuid import UUID
from datetime import datetime


class DriverQueries:
    def __init__(self):
        self.db_client = db_client
        self.hash_helper = HashHelper()

    def create_user(self, user_data: DriverCreate):
        data = dict(user_data.model_dump(exclude_unset=True))
        data["password"] = self.hash_helper.hash_password(data["password"])

        stmt = insert(driver).values(**data).returning(driver)
        result = self.db_client.execute_one(stmt)
        return result

    def get_user_by_id(self, user_id: UUID):
        stmt = select(driver).where(
            and_(driver.c.id == user_id, not driver.c.is_deleted)
        )
        result = self.db_client.execute_one(stmt)
        return result

    def get_user_by_email(self, email: str):
        stmt = select(driver).where(
            and_(driver.c.email == email, driver.c.is_deleted.is_(False))
        )
        result = self.db_client.execute_one(stmt)
        return result

    def update_user(self, user_id: UUID, update_data: dict):
        stmt = (
            update(driver)
            .where(driver.c.id == user_id)
            .values(**update_data)
            .returning(driver)
        )
        result = self.db_client.execute_one(stmt)
        return result

    def soft_delete(self, user_id: UUID):
        stmt = (
            update(driver)
            .where(driver.c.id == user_id)
            .values(is_deleted=True, is_active=False, deleted_at=datetime.now())
            .returning(driver)
        )
        result = self.db_client.execute_one(stmt)
        return result

    def hard_delete_user_by_id(self, user_id: UUID):
        stmt = delete(driver).where(driver.c.id == user_id).returning(driver)
        result = self.db_client.execute_one(stmt)
        return result
