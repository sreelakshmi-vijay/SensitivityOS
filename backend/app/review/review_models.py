from pydantic import BaseModel, Field
from typing import Optional


class ReviewDecision(BaseModel):

    entity: str
    original_sensitivity: str
    corrected_sensitivity: str
    relationship: str
    confidence_adjustment: float = Field(default=0.05, ge=0.0, le=1.0)
    # Optional source/target for precise edge matching
    source: Optional[str] = None
    target: Optional[str] = None
    reviewer_note: Optional[str] = None
