from pydantic import BaseModel


class ReviewDecision(BaseModel):

    entity: str
    original_sensitivity: str
    corrected_sensitivity: str
    relationship: str
    confidence_adjustment: float