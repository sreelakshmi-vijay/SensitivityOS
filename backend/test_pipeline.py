from app.services.classification_pipeline import ClassificationPipeline

pipeline = ClassificationPipeline()

results = pipeline.classify_file(
    "../datasets/sample_hr_data.csv"
)

print(results)