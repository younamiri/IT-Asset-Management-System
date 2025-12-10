from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. models import Location
from .. schemas import LocationCreate, LocationUpdate, LocationResponse

router = APIRouter(prefix="/api/locations", tags=["Locations"])

# ============ GET (خواندن) ============

@router.get("/", response_model=List[LocationResponse])
def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    دریافت تمام مکان‌های دارایی
    """
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """
    دریافت یک مکان دارایی
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="مکان دارایی یافت نشد")
    return location

# ============ POST (ایجاد) ============

@router.post("/", response_model=LocationResponse)
def create_location(location: LocationCreate, db:  Session = Depends(get_db)):
    """
    ایجاد مکان دارایی جدید
    """
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

# ============ PUT (به‌روزرسانی) ============

@router.put("/{location_id}", response_model=LocationResponse)
def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    """
    به‌روزرسانی مکان دارایی
    """
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="مکان دارایی یافت نشد")
    
    update_data = location.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)
    
    db.commit()
    db.refresh(db_location)
    return db_location

# ============ DELETE (حذف) ============

@router.delete("/{location_id}")
def delete_location(location_id:  int, db: Session = Depends(get_db)):
    """
    حذف مکان دارایی
    """
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location: 
        raise HTTPException(status_code=404, detail="مکان دارایی یافت نشد")
    
    db.delete(db_location)
    db.commit()
    return {"message": "مکان دارایی حذف شد"}
