from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent.parent / "review_audit.log"


class AuditLogger:

    @staticmethod
    def log_review(decision):

        timestamp = datetime.now(timezone.utc).isoformat()

        with open(LOG_PATH, "a", encoding="utf-8") as file:

            file.write(
                f"[{timestamp}]\n"
                f"Entity: {decision.entity}\n"
                f"Original: {decision.original_sensitivity}\n"
                f"Corrected: {decision.corrected_sensitivity}\n"
                f"Relationship: {decision.relationship}\n"
                f"Adjustment: {decision.confidence_adjustment}\n"
                f"Source: {decision.source or 'N/A'}\n"
                f"Target: {decision.target or 'N/A'}\n"
                f"Note: {decision.reviewer_note or ''}\n"
                f"-----------------------------------\n"
            )
