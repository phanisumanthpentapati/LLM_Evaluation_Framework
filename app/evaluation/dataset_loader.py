
import json
from pathlib import Path

from app.schemas.dataset_schema import EvaluationTestCase


# Locate the project's datasets folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT / "datasets" / "evaluation_dataset.json"
)


def load_evaluation_dataset():

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with DATASET_PATH.open(
        "r",
        encoding="utf-8"
    ) as file:

        raw_data = json.load(file)

    if not isinstance(raw_data, list):
        raise ValueError(
            "Evaluation dataset must contain a JSON list."
        )

    test_cases = [
        EvaluationTestCase.model_validate(item)
        for item in raw_data
    ]

    return test_cases


def get_dataset_summary():

    test_cases = load_evaluation_dataset()

    summary = {
        "total": len(test_cases),
        "correctness": 0,
        "relevance": 0,
        "groundedness": 0,
        "safety": 0
    }

    for case in test_cases:
        summary[case.category] += 1

    return summary
