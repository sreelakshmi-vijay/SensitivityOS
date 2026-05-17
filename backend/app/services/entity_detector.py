from presidio_analyzer import AnalyzerEngine


class EntityDetector:

    def __init__(self):

        self.analyzer = AnalyzerEngine()

    def detect_entities(self, text: str):

        results = self.analyzer.analyze(
            text=text,
            language="en"
        )

        return results