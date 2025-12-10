from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . config import settings
from .database import Base, engine
from .routes import departments, users, asset_categories, locations, assets, asset_history

# ایجاد تمام جداول در پایگاه‌داده
Base.metadata.create_all(bind=engine)

# ایجاد اپلیکیشن FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="سامانه مدیریت دارایی فناوری اطلاعات"
)

# ============ CORS Middleware ============
# این برای اتصال Frontend به Backend است

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Routers (مسیرها) ============

app.include_router(departments.router)
app.include_router(users.router)
app.include_router(asset_categories.router)
app.include_router(locations.router)
app.include_router(assets.router)
app.include_router(asset_history.router)

# ============ صفحه اصلی ============

@app.get("/")
def read_root():
    """
    صفحه اصلی API
    """
    return {
        "message": "خوش‌آمدید به سامانه مدیریت دارایی فناوری اطلاعات",
        "version": settings.API_VERSION,
        "docs":  "/docs"
    }

@app.get("/health")
def health_check():
    """
    بررسی سلامت سرور
    """
    return {"status": "healthy"}

# ============ شروع سرور ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
