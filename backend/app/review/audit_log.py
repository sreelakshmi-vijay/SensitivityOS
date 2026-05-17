from datetime import datetime


class AuditLogger:

    @staticmethod
    def log_review(decision):

        with open("review_audit.log", "a") as file:

            file.write(
                f"""
[{datetime.utcnow()}]
Entity: {decision.entity}
Original: {decision.original_sensitivity}
Corrected: {decision.corrected_sensitivity}
Relationship: {decision.relationship}
Adjustment: {decision.confidence_adjustment}
-----------------------------------
"""
            )