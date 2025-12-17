from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.config import settings
from .api import auth, tickets, users
import os

app = FastAPI(
    title="IT Helpdesk API",
    description="Система управления заявками для IT поддержки",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание директории для загрузок
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Подключение статических файлов
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Подключение роутеров
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])


@app.get("/")
async def root():
    return {
        "message": "IT Helpdesk API",
        "version": "1.0.0",
        "docs": "/api/docs",
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

if os.path.exists(os.path.join(frontend_path, 'static')):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, 'static')), name="static")

@app.get("/dashboard")
async def dashboard():
    """Serve frontend dashboard"""
    index_path = os.path.join(frontend_path, 'templates', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found"}
