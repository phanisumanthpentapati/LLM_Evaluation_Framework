
class MockLLMProvider:
    """
    Mock LLM provider for development and testing.
    Returns predefined responses without calling an external AI model.
    """

    def generate_response(self, question: str) -> str:

        question_lower = question.lower()

        if "return policy" in question_lower:
            return (
                "Unopened products can be returned "
                "within 10 days."
            )

        elif "capital of india" in question_lower:
            return "The capital of India is New Delhi."

        elif "python" in question_lower:
            return (
                "Python is a high-level, interpreted "
                "programming language."
            )

        else:
            return (
                "I do not have enough information "
                "to answer this question."
            )
