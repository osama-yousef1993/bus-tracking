from src.students.model import StudentCreate
from src.students.query import StudentQueries
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException
from uuid import UUID


class StudentService:
    def __init__(self, queries: StudentQueries):
        self.queries = queries

    async def create_user(self, student_data: StudentCreate):
        existing_student = self.queries.get_user_by_email(student_data.email)
        if existing_student:
            message = {"detail": "Student already exists"}
            return status.HTTP_409_CONFLICT, jsonable_encoder(message)
        try:
            student = self.queries.create_user(student_data)
            if not student:
                message = {"detail": "Could not create student"}
                return status.HTTP_400_BAD_REQUEST, jsonable_encoder(message)
            return status.HTTP_201_CREATED, jsonable_encoder(student)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error creating student: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, None

    async def get_student_by_id(self, student_id: UUID):
        student = self.queries.get_user_by_id(student_id)
        if not student:
            return None
        return student

    async def update_student(self, student_id: UUID, update_data: dict):
        try:
            student = self.queries.update_user(student_id, update_data)
            if not student:
                return None
            return student
        except Exception as e:
            print(f"Error updating student: {e}")
            return None

    async def delete_student(self, student_id: UUID):
        try:
            student = self.queries.soft_delete(student_id)
            if not student:
                return None
            return student
        except Exception as e:
            print(f"Error deleting student: {e}")
            return None
