from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. models import Asset, AssetHistory
from .. schemas import AssetCreate, AssetUpdate, AssetResponse

router = APIRouter(prefix="/api/assets", tags=["Assets"])

# ============ GET (خواندن) ============

@router.get("/", response_model=List[AssetResponse])
def get_assets(skip:  int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    دریافت تمام دارایی‌ها
    """
    assets = db.query(Asset).offset(skip).limit(limit).all()
    return assets

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    دریافت یک دارایی
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="دارایی یافت نشد")
    return asset

@router.get("/category/{category_id}", response_model=List[AssetResponse])
def get_assets_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    دریافت دارایی‌های یک دسته
    """
    assets = db.query(Asset).filter(Asset.category_id == category_id).all()
    return assets

@router.get("/department/{department_id}", response_model=List[AssetResponse])
def get_assets_by_department(department_id: int, db: Session = Depends(get_db)):
    """
    دریافت دارایی‌های یک واحد
    """
    assets = db.query(Asset).filter(Asset.department_id == department_id).all()
    return assets

# ============ POST (ایجاد) ============

@router.post("/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """
    ایجاد دارایی جدید
    """
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# ============ PUT (به‌روزرسانی) ============

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: int, asset: AssetUpdate, db:  Session = Depends(get_db)):
    """
    به‌روزرسانی دارایی
    """
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="دارایی یافت نشد")
    
    update_data = asset.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset

# ============ DELETE (حذف) ============

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    حذف دارایی
    """
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="دارایی یافت نشد")
    
    db.delete(db_asset)
    db.commit()
    return {"message": "دارایی حذف شد"}
