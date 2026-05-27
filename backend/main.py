from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from database import engine

from routers.web_router import router as web_router
from routers.api_reservas_router import router as api_reservas_router
from routers.health_router import router as health_router

app = FastAPI(title="UniSpace API")
app.add_middleware(SessionMiddleware, secret_key="uni-space-secret-key-2026")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(web_router)
app.include_router(api_reservas_router)
app.include_router(health_router)

print("Conexion exitosa con Neon")