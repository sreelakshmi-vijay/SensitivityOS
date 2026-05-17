from app.services.data_scanner import DataScanner
from app.services.entity_detector import EntityDetector
from app.graph.graph_builder import GraphBuilder
from app.graph.inference_engine import InferenceEngine


class ClassificationPipeline:

    ENTITY_MAPPING = {
        "salary": "salary",
        "employee_id": "employee_id",
        "tax_id": "tax_id"
    }

    def __init__(self):

        self.detector = EntityDetector()

        self.graph = GraphBuilder.load_graph(
            "../registry/core/sensitivity_graph.yaml"
        )

    def classify_file(self, file_path: str):

        dataframe = DataScanner.scan_csv(file_path)

        detected_entities = []

        for column in dataframe.columns:

            normalized = column.lower()

            if normalized in self.ENTITY_MAPPING:

                mapped_entity = self.ENTITY_MAPPING[normalized]

                detected_entities.append(mapped_entity)

        inference_results = InferenceEngine.escalate_sensitivity(
            self.graph,
            detected_entities
        )

        return {
            "columns_detected": detected_entities,
            "inference_results": inference_results
        }