from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager

router = APIRouter()

db_manager = get_db_manager()

class DormitoryCreate(BaseModel):
    name: str
    address: str
    description: str

class DormitoryResponse(BaseModel):
    id: int
    name: str
    address: str
    description: str

    class Config:
        from_attributes = True

@router.post("/", response_model=DormitoryResponse)
def create_dormitory(dormitory: DormitoryCreate):
    db_manager.dormitories.add_dormitory(**dormitory.dict())
    return db_manager.dormitories.get_all_dormitories()[-1]

@router.get("/", response_model=list[DormitoryResponse])
def read_dormitories():
    return db_manager.dormitories.get_all_dormitories()

@router.get("/{dormitory_id}", response_model=DormitoryResponse)
def read_dormitory(dormitory_id: int):
    dormitory = db_manager.dormitories.get_dormitory_by_id(dormitory_id)
    if not dormitory:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    return dormitory

@router.put("/{dormitory_id}", response_model=DormitoryResponse)
def update_dormitory(dormitory_id: int, dormitory: DormitoryCreate):
    db_manager.dormitories.update_dormitory(dormitory_id, **dormitory.dict())
    return db_manager.dormitories.get_dormitory_by_id(dormitory_id)

@router.delete("/{dormitory_id}", response_model=DormitoryResponse)
def delete_dormitory(dormitory_id: int):
    dormitory = db_manager.dormitories.get_dormitory_by_id(dormitory_id)
    if not dormitory:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    db_manager.dormitories.delete_dormitory(dormitory_id)
    return dormitory
