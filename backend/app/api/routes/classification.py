from fastapi import APIRouter

from app.services.classification_pipeline import ClassificationPipeline

router = APIRouter()

pipeline = ClassificationPipeline()


@router.get("/classify")

def classify():

    results = pipeline.classify_file(
        "../datasets/sample_hr_data.csv"
    )

    return results