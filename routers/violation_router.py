from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager
from datetime import date

router = APIRouter()

db_manager = get_db_manager()


class ViolationCreate(BaseModel):
    student_id: int
    description: str
    date: date

class ViolationResponse(BaseModel):
    id: int
    student_id: int
    description: str
    violation_date: date

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()  # Преобразуем дату в строку формата 'YYYY-MM-DD'
        }

@router.post("/", response_model=ViolationResponse)
def create_violation(violation: ViolationCreate):
    violation_data = violation.dict()
    db_manager.violations.add_violation(
        student_id=violation_data['student_id'],
        description=violation_data['description'],
        violation_date=violation_data['date']
    )
    return db_manager.violations.get_all_violations()[-1]

@router.get("/", response_model=list[ViolationResponse])
def read_violations():
    return db_manager.violations.get_all_violations()

@router.get("/{violation_id}", response_model=ViolationResponse)
def read_violation(violation_id: int):
    violation = db_manager.violations.get_violation_by_id(violation_id)
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    return violation

@router.put("/{violation_id}", response_model=ViolationResponse)
def update_violation(violation_id: int, violation: ViolationCreate):
    db_manager.violations.update_violation(violation_id, **violation.dict())
    return db_manager.violations.get_violation_by_id(violation_id)

@router.delete("/{violation_id}", response_model=ViolationResponse)
def delete_violation(violation_id: int):
    violation = db_manager.violations.get_violation_by_id(violation_id)
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    db_manager.violations.delete_violation(violation_id)
    return violation
