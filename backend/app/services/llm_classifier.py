import ollama


class LLMClassifier:

    MODEL_NAME = "phi3"

    @classmethod
    def classify_context(
        cls,
        column_name: str,
        nearby_columns: list[str]
    ):

        prompt = f"""
You are a data sensitivity classification engine.

Your task is to determine the sensitivity level
of a database column using contextual reasoning.

COLUMN:
{column_name}

NEARBY COLUMNS:
{", ".join(nearby_columns)}

Return ONLY valid JSON in this format:
Do not include markdown.
Do not include explanation outside JSON.

{{
    "sensitivity": "...",
    "confidence": 0.0,
    "reasoning": "...",
    "needs_human_review": true
}}

Sensitivity levels:
low, medium, high, critical
"""

        response = ollama.chat(
            model=cls.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]