import ollama


class LLMClassifier:

    MODEL_NAME = "phi3"

    @classmethod
    def classify_context(
        cls,
        column_name: str,
        nearby_columns: list
    ):

        prompt = f"""You are a data sensitivity classification engine.

Determine the sensitivity level of a database column using contextual reasoning.

COLUMN: {column_name}

NEARBY COLUMNS IN SAME TABLE: {", ".join(nearby_columns)}

Return ONLY valid JSON. No markdown. No explanation outside the JSON.

{{
    "sensitivity": "...",
    "confidence": 0.0,
    "reasoning": "...",
    "needs_human_review": true
}}

Sensitivity levels (choose exactly one):
- public      — no restrictions; safe to share openly
- internal    — staff-only; low risk if disclosed internally
- confidential — need-to-know; significant risk if exposed (PII, HR data)
- restricted  — regulated data; legal risk if exposed (PHI, PCI, SSN, financials)

Consider: does the column name suggest PII, financial, or health data?
Does the combination of this column with nearby columns elevate sensitivity?
"""

        response = ollama.chat(
            model=cls.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]
