from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..  database import get_db
from ..  models import AssetHistory
from ..  schemas import AssetHistoryCreate, AssetHistoryResponse

router = APIRouter(prefix="/api/asset-history", tags=["Asset History"])

# ============ GET (خواندن) ============

@router.get("/", response_model=List[AssetHistoryResponse])
def get_asset_histories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    دریافت تمام تاریخچه‌های تغییر
    """
    histories = db.query(AssetHistory).offset(skip).limit(limit).all()
    return histories

@router.get("/asset/{asset_id}", response_model=List[AssetHistoryResponse])
def get_asset_history(asset_id: int, db: Session = Depends(get_db)):
    """
    دریافت تاریخچه‌ی تغییرات یک دارایی
    """
    histories = db.query(AssetHistory).filter(AssetHistory.asset_id == asset_id).all()
    return histories

# ============ POST (ایجاد) ============

@router. post("/", response_model=AssetHistoryResponse)
def create_asset_history(history: AssetHistoryCreate, db: Session = Depends(get_db)):
    """
    ثبت تغییر جدید برای دارایی
    """
    db_history = AssetHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
