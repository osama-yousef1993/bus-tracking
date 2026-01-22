from fastapi import APIRouter, Depends
from src.students.model import StudentBase
from src.students.service import StudentService
from uuid import UUID
from fastapi.responses import JSONResponse
from students.query import StudentQueries


router = APIRouter(prefix="/students", tags=["Students"])


def get_student_service():
    return StudentService(StudentQueries())


@router.post("/", response_model=dict)
async def register_student(
    payload: StudentBase,
    service: StudentService = Depends(get_student_service),
):
    status_code, student_data = await service.create_user(payload)
    return JSONResponse(content=student_data, status_code=status_code)


@router.get("/{student_id}", response_model=dict)
async def get_student(
    student_id: UUID,
    service: StudentService = Depends(get_student_service),
):
    student = await service.get_student_by_id(student_id)
    if not student:
        return JSONResponse(content={"detail": "Student not found"}, status_code=404)
    return student
