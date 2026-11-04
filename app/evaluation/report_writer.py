
import json
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"


def save_evaluation_report(report: dict) -> str:
    """
    Save the evaluation report as a JSON file.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report["generated_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    report_path = REPORTS_DIR / "evaluation_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    return str(report_path)
