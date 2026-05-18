from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.classification import router as classification_router, get_pipeline
from app.api.routes.registry import router as registry_router
from app.api.routes.review import router as review_router
from app.api.routes.graph import router as graph_router
from app.api.routes.upload import router as upload_router

# main.py lives at backend/app/main.py — 3 parents = backend/, then go up one more to project root
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_pipeline()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# CORS only needed if someone calls the API from a different origin
# With frontend served by FastAPI itself this is same-origin — keep it open for dev convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# API routes — register BEFORE static mount so /upload etc. take priority
app.include_router(health_router)
app.include_router(classification_router)
app.include_router(registry_router)
app.include_router(review_router)
app.include_router(graph_router)
app.include_router(upload_router)

# Serve frontend — css/, js/ subdirectories
app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
app.mount("/js",  StaticFiles(directory=str(FRONTEND_DIR / "js")),  name="js")


@app.get("/", response_class=FileResponse)
def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))