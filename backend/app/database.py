from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . config import settings

# اتصال به Microsoft SQL Server
DATABASE_URL = f"mssql+pyodbc://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_SERVER}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    وابستگی برای دریافت جلسه پایگاه‌داده
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
