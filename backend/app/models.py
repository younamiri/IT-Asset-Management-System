from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .  database import Base

# ============ Enums ============

class AssetStatus(str, enum.Enum):
    """
    وضعیت دارایی
    """
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    MAINTENANCE = "تعمیر و نگهداری"
    RETIRED = "بازنشسته"
    DAMAGED = "خراب"

class AssetType(str, enum.Enum):
    """
    نوع دارایی
    """
    PHYSICAL_SERVER = "سرور فیزیکی"
    VIRTUAL_SERVER = "سرور مجازی"
    FIREWALL = "فایروال"
    ALL_IN_ONE = "All In One"
    PHONE = "تلفن"
    LAPTOP = "لپ‌تاپ"
    DESKTOP = "کامپیوتر رومیزی"
    PRINTER = "پرینتر"
    NETWORK_SWITCH = "سوئیچ شبکه"
    ROUTER = "روتر"
    UPS = "UPS"
    OTHER = "سایر"

# ============ Models ============

class Department(Base):
    """
    واحدهای سازمانی
    """
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("departments.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # روابط
    parent = relationship("Department", remote_side=[id])
    users = relationship("User", back_populates="department")
    assets = relationship("Asset", back_populates="department")

class User(Base):
    """
    کاربران سامانه
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    ad_user_id = Column(String(100))  # Active Directory User ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # روابط
    department = relationship("Department", back_populates="users")
    assets = relationship("Asset", back_populates="owner")
    histories = relationship("AssetHistory", back_populates="user")

class AssetCategory(Base):
    """
    دسته‌های دارایی
    """
    __tablename__ = "asset_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    asset_type = Column(String(50), nullable=False)  # نوع دارایی
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # روابط
    assets = relationship("Asset", back_populates="category")

class Location(Base):
    """
    مکان‌های دارایی
    """
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    building = Column(String(50))
    floor = Column(Integer)
    room = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # روابط
    assets = relationship("Asset", back_populates="location")

class Asset(Base):
    """
    دارایی‌های فناوری اطلاعات
    """
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_number = Column(String(50), unique=True, nullable=False)  # شماره دارایی
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("asset_categories.id"), nullable=False)
    asset_type = Column(String(50), nullable=False)
    status = Column(String(20), default=AssetStatus.ACTIVE)
    
    # اطلاعات مالی
    purchase_date = Column(DateTime)
    purchase_price = Column(Float)
    depreciation_rate = Column(Float, default=0.0)
    warranty_expiry = Column(DateTime)
    
    # مالک و مکان
    owner_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    
    # مشخصات فنی
    serial_number = Column(String(100), unique=True)
    model = Column(String(100))
    manufacturer = Column(String(100))
    
    # تاریخچه
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # روابط
    category = relationship("AssetCategory", back_populates="assets")
    owner = relationship("User", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    location = relationship("Location", back_populates="assets")
    histories = relationship("AssetHistory", back_populates="asset")

class AssetHistory(Base):
    """
    تاریخچه تغییرات دارایی
    """
    __tablename__ = "asset_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    change_type = Column(String(50))  # مثل:  نقل مکان، تعویض مالک، تعمیر
    old_value = Column(Text)  # مقدار قبلی
    new_value = Column(Text)  # مقدار جدید
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # روابط
    asset = relationship("Asset", back_populates="histories")
    user = relationship("User", back_populates="histories")

class Report(Base):
    """
    گزارش‌های سامانه
    """
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    report_type = Column(String(50))  # مثل: دارایی_واحد، دارایی_پرسنل
    filters = Column(Text)  # فیلترهای گزارش (JSON)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
