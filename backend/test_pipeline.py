from pathlib import Path
from app.services.classification_pipeline import ClassificationPipeline

# Resolve dataset path relative to this file so the test works from any cwd
DATASET_PATH = str(Path(__file__).resolve().parent.parent / "datasets" / "sample_hr_data.csv")

pipeline = ClassificationPipeline()
results = pipeline.classify_file(DATASET_PATH)
print(results)
