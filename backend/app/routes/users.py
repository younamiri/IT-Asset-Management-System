from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. models import User
from .. schemas import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from .. auth import create_access_token
from datetime import timedelta
from .. config import settings

router = APIRouter(prefix="/api/users", tags=["Users"])

# ============ GET (خواندن) ============

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit:  int = 100, db: Session = Depends(get_db)):
    """
    دریافت تمام کاربران
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    دریافت یک کاربر
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    return user

# ============ POST (ایجاد) ============

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    ایجاد کاربر جدید
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="نام کاربری قبلاً استفاده شده است")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    ورود کاربر
    """
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user: 
        raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")
    
    # توکن ایجاد کنید
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ============ PUT (به‌روزرسانی) ============

@router. put("/{user_id}", response_model=UserResponse)
def update_user(user_id:  int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    به‌روزرسانی کاربر
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user: 
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    
    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# ============ DELETE (حذف) ============

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    حذف کاربر
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    
    db.delete(db_user)
    db.commit()
    return {"message": "کاربر حذف شد"}
