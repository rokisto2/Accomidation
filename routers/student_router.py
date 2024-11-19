from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager

router = APIRouter()
db_manager = get_db_manager()

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    contact_info: str
    course: int
    grup: int
    is_non_local: bool
    password: str
    gender: str

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    contact_info: str
    course: int
    grup: int
    is_non_local: bool
    gender: str

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate):
    db_manager.students.add_student(**student.dict())
    new_student = db_manager.students.get_all_students()[-1]
    return new_student

@router.get("/", response_model=list[StudentResponse])
def read_students():
    return db_manager.students.get_all_students()

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int):
    student = db_manager.students.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate):
    db_manager.students.update_student(student_id, **student.dict())
    return db_manager.students.get_student_by_id(student_id)

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int):
    student = db_manager.students.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_manager.students.delete_student(student_id)
    return student

@router.get("/unassigned", response_model=list[StudentResponse])
def read_unassigned_students():
    unassigned_students = db_manager.students.get_unassigned_students()
    return [StudentResponse.from_orm(student) for student in unassigned_students]