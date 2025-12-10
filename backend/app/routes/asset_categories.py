from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. models import AssetCategory
from .. schemas import AssetCategoryCreate, AssetCategoryUpdate, AssetCategoryResponse

router = APIRouter(prefix="/api/asset-categories", tags=["Asset Categories"])

# ============ GET (خواندن) ============

@router.get("/", response_model=List[AssetCategoryResponse])
def get_asset_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    دریافت تمام دسته‌های دارایی
    """
    categories = db.query(AssetCategory).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=AssetCategoryResponse)
def get_asset_category(category_id:  int, db: Session = Depends(get_db)):
    """
    دریافت یک دسته دارایی
    """
    category = db.query(AssetCategory).filter(AssetCategory. id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="دسته دارایی یافت نشد")
    return category

# ============ POST (ایجاد) ============

@router.post("/", response_model=AssetCategoryResponse)
def create_asset_category(category:  AssetCategoryCreate, db:  Session = Depends(get_db)):
    """
    ایجاد دسته دارایی جدید
    """
    db_category = AssetCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# ============ PUT (به‌روزرسانی) ============

@router.put("/{category_id}", response_model=AssetCategoryResponse)
def update_asset_category(category_id: int, category: AssetCategoryUpdate, db: Session = Depends(get_db)):
    """
    به‌روزرسانی دسته دارایی
    """
    db_category = db. query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="دسته دارایی یافت نشد")
    
    update_data = category.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

# ============ DELETE (حذف) ============

@router.delete("/{category_id}")
def delete_asset_category(category_id: int, db: Session = Depends(get_db)):
    """
    حذف دسته دارایی
    """
    db_category = db. query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="دسته دارایی یافت نشد")
    
    db.delete(db_category)
    db.commit()
    return {"message":  "دسته دارایی حذف شد"}
