from fastapi import FastAPI

from routers.web_router import router as web_router
from routers.api_reservas_router import router as api_reservas_router
from routers.health_router import router as health_router

app = FastAPI(title="UniSpace API")

app.include_router(web_router)
app.include_router(api_reservas_router)
app.include_router(health_router)