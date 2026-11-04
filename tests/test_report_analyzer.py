
from app.evaluation.report_analyzer import analyze_evaluation_report


def test_report_analyzer_counts_metrics():

    report = {
        "total_test_cases": 2,
        "passed_test_cases": 1,
        "failed_test_cases": 1,
        "pass_rate": 50.0,
        "results": [
            {
                "test_case_id": "TC001",
                "question": "What is Python?",
                "actual_output": "Python is a programming language.",
                "overall_passed": True,
                "metrics": [
                    {"metric": "correctness", "score": 1.0, "passed": True},
                    {"metric": "safety", "score": 1.0, "passed": True}
                ]
            },
            {
                "test_case_id": "TC002",
                "question": "What is Java?",
                "actual_output": "Java is a fruit.",
                "overall_passed": False,
                "metrics": [
                    {"metric": "correctness", "score": 0.0, "passed": False},
                    {"metric": "safety", "score": 1.0, "passed": True}
                ]
            }
        ]
    }

    analysis = analyze_evaluation_report(report)

    assert analysis["total_test_cases"] == 2
    assert analysis["passed_test_cases"] == 1
    assert analysis["failed_test_cases"] == 1

    assert analysis["metric_summary"]["correctness"]["passed"] == 1
    assert analysis["metric_summary"]["correctness"]["failed"] == 1

    assert analysis["metric_summary"]["safety"]["passed"] == 2

    assert len(analysis["failed_case_details"]) == 1
    assert analysis["failed_case_details"][0]["test_case_id"] == "TC002"


def test_metric_pass_rate():

    report = {
        "total_test_cases": 2,
        "passed_test_cases": 1,
        "failed_test_cases": 1,
        "pass_rate": 50.0,
        "results": [
            {
                "test_case_id": "TC001",
                "question": "Question 1",
                "actual_output": "Answer 1",
                "overall_passed": True,
                "metrics": [
                    {"metric": "correctness", "score": 1.0, "passed": True}
                ]
            },
            {
                "test_case_id": "TC002",
                "question": "Question 2",
                "actual_output": "Answer 2",
                "overall_passed": False,
                "metrics": [
                    {"metric": "correctness", "score": 0.0, "passed": False}
                ]
            }
        ]
    }

    analysis = analyze_evaluation_report(report)

    assert analysis["metric_summary"]["correctness"]["pass_rate"] == 50.0
