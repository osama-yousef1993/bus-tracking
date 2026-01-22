from sqlalchemy import select, insert, update, delete, and_
from src.database.schema import students
from src.authentications.hash import HashHelper
from src.database.execution import db_client
from src.students.model import StudentBase
from uuid import UUID
from datetime import datetime


class StudentQueries:
    def __init__(self):
        self.db_client = db_client
        self.hash_helper = HashHelper()

    def create_user(self, user_data: StudentBase):
        data = dict(user_data.model_dump(exclude_unset=True))
        data["password"] = self.hash_helper.hash_password(data["password"])

        stmt = insert(students).values(**data).returning(students)
        result = self.db_client.execute_one(stmt)
        return result

    def get_user_by_id(self, user_id: UUID):
        stmt = select(students).where(
            and_(students.c.id == user_id, not students.c.is_deleted)
        )
        result = self.db_client.execute_one(stmt)
        return result

    def get_user_by_email(self, email: str):
        stmt = select(students).where(
            and_(students.c.email == email, students.c.is_deleted.is_(False))
        )
        result = self.db_client.execute_one(stmt)
        return result

    def update_user(self, user_id: UUID, update_data: dict):
        stmt = (
            update(students)
            .where(students.c.id == user_id)
            .values(**update_data)
            .returning(students)
        )
        result = self.db_client.execute_one(stmt)
        return result

    def soft_delete(self, user_id: UUID):
        stmt = (
            update(students)
            .where(students.c.id == user_id)
            .values(is_deleted=True, is_active=False, deleted_at=datetime.now())
            .returning(students)
        )
        result = self.db_client.execute_one(stmt)
        return result

    def hard_delete_user_by_id(self, user_id: UUID):
        stmt = delete(students).where(students.c.id == user_id).returning(students)
        result = self.db_client.execute_one(stmt)
        return result
