from app.deepeval.metrics import check_answer_relevancy


def test_relevant_answer():
    result = check_answer_relevancy(
        "What is Python?",
        "Python is a programming language."
    )

    assert result["metric"] == "Answer Relevancy"
    assert result["passed"] is True


def test_irrelevant_answer():
    result = check_answer_relevancy(
        "What is Python?",
        "The capital of India is New Delhi."
    )

    assert result["passed"] is False