from fastapi import APIRouter
from app.review.audit_log import AuditLogger
from app.review.review_models import ReviewDecision
from app.review.feedback_engine import FeedbackEngine

router = APIRouter()


@router.post("/review/submit")
def submit_review(decision: ReviewDecision):

    result = FeedbackEngine.update_graph_weights(
        "../registry/core/sensitivity_graph.yaml",
        decision
    )

    AuditLogger.log_review(decision)

    return {
        "message": "Review processed",
        "result": result
    }