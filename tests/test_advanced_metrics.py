
from app.evaluation.advanced_metrics import (
    faithfulness_metric,
    hallucination_metric
)


def test_faithfulness_with_supported_answer():
    result = faithfulness_metric(
        "Employees receive 20 annual leave days.",
        "Employees receive 20 annual leave days."
    )

    assert result["passed"] is True
    assert result["score"] == 1.0


def test_faithfulness_with_unsupported_answer():
    result = faithfulness_metric(
        "Employees receive 30 annual leave days.",
        "Employees receive 20 annual leave days."
    )

    assert result["passed"] is False


def test_hallucination_with_supported_answer():
    result = hallucination_metric(
        "Employees receive 20 annual leave days.",
        "Employees receive 20 annual leave days."
    )

    assert result["passed"] is True
    assert result["score"] == 0.0


def test_hallucination_with_unsupported_answer():
    result = hallucination_metric(
        "Employees receive 30 annual leave days.",
        "Employees receive 20 annual leave days."
    )

    assert result["passed"] is False
