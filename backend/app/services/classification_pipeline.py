import json
from pathlib import Path

from app.services.data_scanner import DataScanner
from app.services.entity_detector import EntityDetector
from app.graph.graph_builder import GraphBuilder
from app.graph.inference_engine import InferenceEngine
from app.services.llm_classifier import LLMClassifier
from app.review.review_queue import ReviewQueue

# classification_pipeline.py lives at backend/app/services/
# 4 x .parent → project root
REGISTRY_PATH = str(Path(__file__).resolve().parent.parent.parent.parent / "registry")

SENSITIVITY_ORDER = {
    "public": 1,
    "internal": 2,
    "confidential": 3,
    "restricted": 4,
}

# Map Presidio entity types → (graph_node_id, sensitivity_tier)
PRESIDIO_SENSITIVITY_MAP = {
    "PERSON":          ("name",          "confidential"),
    "EMAIL_ADDRESS":   ("email",         "confidential"),
    "PHONE_NUMBER":    ("phone_number",  "confidential"),
    "LOCATION":        ("location",      "internal"),
    "DATE_TIME":       ("date",          "internal"),
    "NRP":             ("nationality",   "confidential"),
    "MEDICAL_LICENSE": ("medical_id",    "restricted"),
    "US_SSN":          ("ssn",           "restricted"),
    "CREDIT_CARD":     ("credit_card",   "restricted"),
    "IBAN_CODE":       ("bank_account",  "restricted"),
    "US_BANK_NUMBER":  ("bank_account",  "restricted"),
    "IP_ADDRESS":      ("ip_address",    "internal"),
    "URL":             ("url",           "public"),
}


class ClassificationPipeline:

    def __init__(self):
        self.detector = EntityDetector()
        self.graph = GraphBuilder.load_graph(REGISTRY_PATH)

    def classify_file(self, file_path: str):

        dataframe = DataScanner.scan_csv(file_path)

        detected_entities = []
        presidio_results = {}
        llm_results = {}

        all_columns = [col.lower().strip() for col in dataframe.columns]

        for column in dataframe.columns:

            normalized = column.lower().strip()

            # ── Layer 1: Presidio — scan sampled cell values for PII ──────
            sample_values = (
                dataframe[column]
                .dropna()
                .astype(str)
                .head(20)
                .tolist()
            )
            sample_text = " ".join(sample_values)

            presidio_entities = self.detector.detect_entities(sample_text)

            # FIX: collect all hits first, then pick the highest-severity one
            hits = []
            for result in presidio_entities:
                entity_type = result.entity_type
                if entity_type in PRESIDIO_SENSITIVITY_MAP:
                    node_id, sensitivity = PRESIDIO_SENSITIVITY_MAP[entity_type]
                    hits.append({
                        "entity_type": entity_type,
                        "node_id": node_id,
                        "sensitivity": sensitivity,
                        "confidence": round(result.score, 3),
                        "source": "presidio",
                    })

            # Pick the hit with the highest sensitivity tier (then highest confidence)
            presidio_hit = None
            if hits:
                presidio_hit = max(
                    hits,
                    key=lambda h: (
                        SENSITIVITY_ORDER.get(h["sensitivity"], 0),
                        h["confidence"],
                    ),
                )

            presidio_results[normalized] = presidio_hit

            # ── Layer 2: Graph — match column name against known nodes ─────
            if normalized in self.graph.nodes:
                detected_entities.append(normalized)

            # ── Layer 3: LLM — only when Presidio confidence is low ───────
            presidio_confident = (
                presidio_hit is not None
                and presidio_hit["confidence"] >= 0.80
            )

            if not presidio_confident:
                nearby_columns = [c for c in all_columns if c != normalized]

                # FIX: wrap in try/except — Ollama being offline must not crash the request
                try:
                    raw_response = LLMClassifier.classify_context(
                        normalized, nearby_columns
                    )
                    parsed = json.loads(raw_response)
                    parsed["sensitivity"] = _normalise_sensitivity(
                        parsed.get("sensitivity", "public")
                    )
                    parsed["source"] = "llm"

                except Exception as exc:
                    # LLM unavailable or returned invalid JSON — degrade gracefully
                    parsed = {
                        "sensitivity": "public",
                        "confidence": 0.0,
                        "reasoning": f"LLM unavailable or parse error: {exc}",
                        "needs_human_review": True,
                        "source": "llm_error",
                    }

                llm_results[normalized] = parsed

        # ── Graph inference (contextual escalation) ───────────────────────
        inference_results = InferenceEngine.escalate_sensitivity(
            self.graph, detected_entities
        )

        # ── Merge all three layers into one classification per column ─────
        final_classifications = {}
        review_items = {}

        for col in all_columns:

            presidio  = presidio_results.get(col)
            graph_inf = inference_results.get(col)
            llm       = llm_results.get(col)

            final_sensitivity, confidence, sources = _merge_layers(
                presidio, graph_inf, llm
            )

            needs_review = ReviewQueue.should_review(confidence)

            entry = {
                "final_sensitivity": final_sensitivity,
                "confidence": round(confidence, 3),
                "sources_used": sources,
                "needs_human_review": needs_review,
                "presidio": presidio,
                "graph_inference": graph_inf,
                "llm_analysis": llm,
            }

            final_classifications[col] = entry

            if needs_review:
                review_items[col] = entry

        return {
            "columns_detected": detected_entities,
            "graph_inference": inference_results,
            "llm_analysis": llm_results,
            "final_classifications": final_classifications,
            "review_queue": review_items,
        }


def _normalise_sensitivity(raw: str) -> str:
    mapping = {
        "low": "public", "none": "public", "public": "public",
        "medium": "internal", "internal": "internal",
        "high": "confidential", "confidential": "confidential",
        "critical": "restricted", "restricted": "restricted",
    }
    return mapping.get(raw.lower().strip(), "public")


def _merge_layers(presidio, graph_inf, llm):
    """
    Merge three classification sources into one sensitivity + confidence.
    Highest tier wins. Multiple agreeing sources boost confidence.
    """
    candidates = []

    if presidio:
        candidates.append((presidio["sensitivity"], presidio["confidence"], "presidio"))

    if graph_inf:
        # Graph inference is deterministic — assign fixed high confidence
        candidates.append((graph_inf["final_sensitivity"], 0.90, "graph"))

    if llm and llm.get("source") != "llm_error":
        candidates.append((
            llm.get("sensitivity", "public"),
            float(llm.get("confidence", 0.5)),
            "llm",
        ))

    if not candidates:
        return "public", 0.0, []

    # Highest sensitivity tier wins
    candidates.sort(key=lambda c: SENSITIVITY_ORDER.get(c[0], 0), reverse=True)
    top_sensitivity = candidates[0][0]

    # Sources that agree on the top tier
    agreeing = [c for c in candidates if c[0] == top_sensitivity]
    base_confidence = max(c[1] for c in agreeing)

    # Each additional agreeing source adds 10% confidence (capped at 1.0)
    if len(agreeing) > 1:
        base_confidence = min(base_confidence + 0.10 * (len(agreeing) - 1), 1.0)

    sources_used = [c[2] for c in agreeing]

    return top_sensitivity, base_confidence, sources_used
