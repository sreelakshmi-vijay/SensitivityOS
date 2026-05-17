from fastapi import FastAPI
from app.api.routes.registry import router as registry_router
from app.api.routes.health import router as health_router
from app.api.routes.classification import router as classification_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(health_router)
app.include_router(classification_router)
app.include_router(registry_router)