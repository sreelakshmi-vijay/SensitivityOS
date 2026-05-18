import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.api.routes.classification import get_pipeline

router = APIRouter()

# upload.py lives at backend/app/api/routes/upload.py
# 5 x .parent  →  project root
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "uploads"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pipeline = get_pipeline()
    results = pipeline.classify_file(str(file_path))

    return {
        "filename": file.filename,
        "results": results,
    }
