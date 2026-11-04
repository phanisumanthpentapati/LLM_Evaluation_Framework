
from app.evaluation.evaluator import run_evaluation


def test_evaluation_returns_all_dataset_cases():
    report = run_evaluation()

    assert report["total_test_cases"] == 6
    assert len(report["results"]) == 6


def test_evaluation_has_valid_pass_rate():
    report = run_evaluation()

    assert 0 <= report["pass_rate"] <= 100


def test_evaluation_contains_seven_metrics():
    report = run_evaluation()

    expected_metrics = {
        "correctness",
        "relevance",
        "groundedness",
        "safety",
        "Answer Relevancy",
        "Faithfulness",
        "Hallucination"
    }

    for result in report["results"]:
        assert len(result["metrics"]) == 7

        actual_metrics = {
            metric["metric"]
            for metric in result["metrics"]
        }

        assert actual_metrics == expected_metrics


def test_correct_response_passes_correctness():
    report = run_evaluation()

    for result in report["results"]:
        correctness = next(
            metric
            for metric in result["metrics"]
            if metric["metric"] == "correctness"
        )

        assert correctness["passed"] is True
