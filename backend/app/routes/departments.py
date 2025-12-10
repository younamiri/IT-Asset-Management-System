from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..  database import get_db
from ..  models import Department
from .. schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter(prefix="/api/departments", tags=["Departments"])

# ============ GET (خواندن) ============

@router. get("/", response_model=List[DepartmentResponse])
def get_departments(skip: int = 0, limit:  int = 100, db: Session = Depends(get_db)):
    """
    دریافت تمام واحدهای سازمانی
    """
    departments = db.query(Department).offset(skip).limit(limit).all()
    return departments

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    """
    دریافت یک واحد سازمانی
    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department: 
        raise HTTPException(status_code=404, detail="واحد سازمانی یافت نشد")
    return department

# ============ POST (ایجاد) ============

@router.post("/", response_model=DepartmentResponse)
def create_department(department: DepartmentCreate, db:  Session = Depends(get_db)):
    """
    ایجاد واحد سازمانی جدید
    """
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

# ============ PUT (به‌روزرسانی) ============

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    """
    به‌روزرسانی واحد سازمانی
    """
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="واحد سازمانی یافت نشد")
    
    update_data = department.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_department, field, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department

# ============ DELETE (حذف) ============

@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    """
    حذف واحد سازمانی
    """
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="واحد سازمانی یافت نشد")
    
    db.delete(db_department)
    db.commit()
    return {"message": "واحد سازمانی حذف شد"}
