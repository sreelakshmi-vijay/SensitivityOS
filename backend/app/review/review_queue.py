class ReviewQueue:

    @staticmethod
    def should_review(confidence: float):

        return confidence < 0.75