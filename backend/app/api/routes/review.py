from pathlib import Path
from fastapi import APIRouter
from app.review.audit_log import AuditLogger
from app.review.review_models import ReviewDecision
from app.review.feedback_engine import FeedbackEngine

router = APIRouter()

# review.py lives at backend/app/api/routes/review.py
# 4 x .parent → backend/, then one more → project root
CORE_GRAPH_PATH = str(
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "registry" / "core" / "sensitivity_graph.yaml"
)

@router.post("/review/submit")
def submit_review(decision: ReviewDecision):
    result = FeedbackEngine.update_graph_weights(CORE_GRAPH_PATH, decision)
    AuditLogger.log_review(decision)
    return {
        "message": "Review processed",
        "result": result
    }
