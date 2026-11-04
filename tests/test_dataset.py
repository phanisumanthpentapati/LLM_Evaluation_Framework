
import pytest

from app.evaluation.dataset_loader import (
    load_evaluation_dataset,
    get_dataset_summary
)


def test_dataset_loads_successfully():

    test_cases = load_evaluation_dataset()

    assert len(test_cases) == 6


def test_dataset_contains_required_categories():

    test_cases = load_evaluation_dataset()

    categories = {
        case.category for case in test_cases
    }

    assert categories == {
        "correctness",
        "relevance",
        "groundedness",
        "safety"
    }


def test_every_test_case_has_unique_id():

    test_cases = load_evaluation_dataset()

    ids = [case.id for case in test_cases]

    assert len(ids) == len(set(ids))


def test_dataset_summary():

    summary = get_dataset_summary()

    assert summary["total"] == 6
    assert summary["correctness"] == 2
    assert summary["relevance"] == 2
    assert summary["groundedness"] == 1
    assert summary["safety"] == 1


def test_dataset_questions_are_not_empty():

    test_cases = load_evaluation_dataset()

    for case in test_cases:
        assert len(case.question.strip()) >= 3
