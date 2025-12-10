from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ============ Department Schemas ============

class DepartmentBase(BaseModel):
    """
    پایه‌ی Department
    """
    name: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    """
    ایجاد Department جدید
    """
    pass

class DepartmentUpdate(BaseModel):
    """
    به‌روزرسانی Department
    """
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None

class DepartmentResponse(DepartmentBase):
    """
    پاسخ Department
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============ User Schemas ============

class UserBase(BaseModel):
    """
    پایه‌ی User
    """
    username: str
    email: EmailStr
    full_name: str
    department_id: Optional[int] = None
    is_admin: bool = False
    ad_user_id: Optional[str] = None

class UserCreate(UserBase):
    """
    ایجاد User جدید
    """
    password:  str

class UserUpdate(BaseModel):
    """
    به‌روزرسانی User
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    department_id: Optional[int] = None
    is_admin: Optional[bool] = None

class UserResponse(UserBase):
    """
    پاسخ User
    """
    id: int
    is_active: bool
    created_at:  datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """
    ورود کاربر
    """
    username: str
    password: str

class Token(BaseModel):
    """
    توکن JWT
    """
    access_token: str
    token_type:  str = "bearer"

# ============ AssetCategory Schemas ============

class AssetCategoryBase(BaseModel):
    """
    پایه‌ی AssetCategory
    """
    name: str
    description: Optional[str] = None
    asset_type: str

class AssetCategoryCreate(AssetCategoryBase):
    """
    ایجاد AssetCategory جدید
    """
    pass

class AssetCategoryUpdate(BaseModel):
    """
    به‌روزرسانی AssetCategory
    """
    name: Optional[str] = None
    description: Optional[str] = None
    asset_type: Optional[str] = None

class AssetCategoryResponse(AssetCategoryBase):
    """
    پاسخ AssetCategory
    """
    id: int
    created_at:  datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============ Location Schemas ============

class LocationBase(BaseModel):
    """
    پایه‌ی Location
    """
    name: str
    building: Optional[str] = None
    floor: Optional[int] = None
    room: Optional[str] = None
    description: Optional[str] = None

class LocationCreate(LocationBase):
    """
    ایجاد Location جدید
    """
    pass

class LocationUpdate(BaseModel):
    """
    به‌روزرسانی Location
    """
    name: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[int] = None
    room: Optional[str] = None
    description: Optional[str] = None

class LocationResponse(LocationBase):
    """
    پاسخ Location
    """
    id: int
    created_at:  datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============ Asset Schemas ============

class AssetBase(BaseModel):
    """
    پایه‌ی Asset
    """
    asset_number: str
    name: str
    description: Optional[str] = None
    category_id: int
    asset_type: str
    status: str = "فعال"
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    depreciation_rate:  Optional[float] = 0.0
    warranty_expiry: Optional[datetime] = None
    owner_id: Optional[int] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    serial_number: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None

class AssetCreate(AssetBase):
    """
    ایجاد Asset جدید
    """
    pass

class AssetUpdate(BaseModel):
    """
    به‌روزرسانی Asset
    """
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    owner_id: Optional[int] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    warranty_expiry: Optional[datetime] = None

class AssetResponse(AssetBase):
    """
    پاسخ Asset
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True

# ============ AssetHistory Schemas ============

class AssetHistoryBase(BaseModel):
    """
    پایه‌ی AssetHistory
    """
    asset_id: int
    user_id: int
    change_type: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    description: Optional[str] = None

class AssetHistoryCreate(AssetHistoryBase):
    """
    ایجاد AssetHistory جدید
    """
    pass

class AssetHistoryResponse(AssetHistoryBase):
    """
    پاسخ AssetHistory
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Report Schemas ============

class ReportBase(BaseModel):
    """
    پایه‌ی Report
    """
    title: str
    report_type: str
    filters: Optional[str] = None

class ReportCreate(ReportBase):
    """
    ایجاد Report جدید
    """
    pass

class ReportResponse(ReportBase):
    """
    پاسخ Report
    """
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True

# ============ Dashboard Schemas ============

class DashboardStats(BaseModel):
    """
    آمار داشبورد
    """
    total_assets: int
    active_assets: int
    inactive_assets: int
    maintenance_assets: int
    retired_assets: int
    total_value: float
    total_departments: int
    total_users:  int

class DepartmentDashboard(BaseModel):
    """
    داشبورد واحد
    """
    department_name: str
    total_assets:  int
    assets_by_type: dict
    total_value: float
    recent_changes: List[AssetHistoryResponse]

class PersonalDashboard(BaseModel):
    """
    داشبورد پرسنل
    """
    user_name: str
    my_assets: List[AssetResponse]
    total_assets_count: int
    total_assets_value: float
    recent_changes: List[AssetHistoryResponse]
