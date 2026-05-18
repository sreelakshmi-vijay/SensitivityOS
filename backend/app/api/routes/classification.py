from fastapi import APIRouter, HTTPException, Query
from pathlib import Path

router = APIRouter()

# Import lazily inside the route so the pipeline singleton is created once
_pipeline = None


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        from app.services.classification_pipeline import ClassificationPipeline
        _pipeline = ClassificationPipeline()
    return _pipeline


@router.get("/classify")
def classify(path: str = Query(..., description="Absolute or relative path to a CSV file")):
    """
    Classify a CSV file by path.
    Use POST /upload to classify a file by uploading it directly.
    """
    csv_path = Path(path)

    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path}")

    if csv_path.suffix.lower() != ".csv":
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    pipeline = get_pipeline()
    return pipeline.classify_file(str(csv_path))
