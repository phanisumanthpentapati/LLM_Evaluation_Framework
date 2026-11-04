
import json

from app.evaluation.report_writer import save_evaluation_report


def test_save_evaluation_report(tmp_path, monkeypatch):
    import app.evaluation.report_writer as writer

    # Use a temporary directory for testing
    monkeypatch.setattr(writer, "REPORTS_DIR", tmp_path)

    report = {
        "total_test_cases": 6,
        "passed_test_cases": 6,
        "failed_test_cases": 0,
        "pass_rate": 100.0
    }

    # Save the report
    report_path = save_evaluation_report(report)

    # Read the generated JSON file
    with open(report_path, "r", encoding="utf-8") as file:
        saved_report = json.load(file)

    # Validate the saved report
    assert saved_report["total_test_cases"] == 6
    assert saved_report["passed_test_cases"] == 6
    assert saved_report["failed_test_cases"] == 0
    assert saved_report["pass_rate"] == 100.0
    assert "generated_at" in saved_report
