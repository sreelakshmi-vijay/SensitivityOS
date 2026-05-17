from app.services.data_scanner import DataScanner
from app.services.entity_detector import EntityDetector
from app.graph.graph_builder import GraphBuilder
from app.graph.inference_engine import InferenceEngine
import json

from app.services.llm_classifier import LLMClassifier
from app.review.review_queue import ReviewQueue

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

        llm_results = {}

        for column in dataframe.columns:

            normalized = column.lower()

            nearby_columns = [
                col.lower()
                for col in dataframe.columns
                if col.lower() != normalized
            ]

            llm_response = LLMClassifier.classify_context(
                normalized,
                nearby_columns
            )

            try:

                parsed_response = json.loads(llm_response)

            except Exception:

                parsed_response = {
                    "sensitivity": "unknown",
                    "confidence": 0.0,
                    "reasoning": "Failed to parse LLM response",
                    "needs_human_review": True
                }

            llm_results[normalized] = parsed_response

            if normalized in self.ENTITY_MAPPING:

                mapped_entity = self.ENTITY_MAPPING[normalized]

                detected_entities.append(mapped_entity)

        inference_results = InferenceEngine.escalate_sensitivity(
            self.graph,
            detected_entities
        )

        review_items = {}

        for column, result in llm_results.items():

            confidence = result.get("confidence", 0.0)

            if ReviewQueue.should_review(confidence):

                review_items[column] = result

        return {
            "columns_detected": detected_entities,
            "graph_inference": inference_results,
            "llm_analysis": llm_results,
            "review_queue": review_items
        }