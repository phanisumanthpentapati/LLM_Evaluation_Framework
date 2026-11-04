
from app.evaluation.dataset_loader import load_evaluation_dataset

from app.evaluation.metrics import (
    correctness_metric,
    relevance_metric,
    groundedness_metric,
    safety_metric
)

from app.deepeval.metrics import check_answer_relevancy

from app.evaluation.advanced_metrics import (
    faithfulness_metric,
    hallucination_metric
)

from app.llm.provider import MockLLMProvider


# Metrics that must pass for an answer to be accepted
CRITICAL_METRICS = {
    "correctness",
    "safety",
    "groundedness",
    "Faithfulness",
    "Hallucination"
}


def get_answer_decision(metrics):
    """
    Determine whether an AI-generated answer is acceptable.

    ACCEPT: All seven metrics pass.
    REVIEW: Only non-critical metrics fail.
    REJECT: At least one critical metric fails.
    """

    failed_metrics = [
        metric["metric"]
        for metric in metrics
        if not metric["passed"]
    ]

    critical_failures = [
        name for name in failed_metrics
        if name in CRITICAL_METRICS
    ]

    if critical_failures:
        return {
            "decision": "REJECT",
            "reason": (
                "Critical quality checks failed: "
                + ", ".join(critical_failures)
            )
        }

    if failed_metrics:
        return {
            "decision": "REVIEW",
            "reason": (
                "Non-critical quality checks require review: "
                + ", ".join(failed_metrics)
            )
        }

    return {
        "decision": "ACCEPT",
        "reason": "All seven evaluation checks passed."
    }


def evaluate_test_case(test_case, actual_output):

    correctness = correctness_metric(
        actual_output,
        test_case.expected_answer
    )

    relevance = relevance_metric(
        test_case.question,
        actual_output
    )

    groundedness = groundedness_metric(
        actual_output,
        test_case.context
    )

    safety = safety_metric(
        actual_output,
        test_case.should_refuse
    )

    answer_relevancy = check_answer_relevancy(
        test_case.question,
        actual_output
    )

    faithfulness = faithfulness_metric(
        actual_output,
        test_case.context
    )

    hallucination = hallucination_metric(
        actual_output,
        test_case.context
    )

    results = [
        correctness,
        relevance,
        groundedness,
        safety,
        answer_relevancy,
        faithfulness,
        hallucination
    ]

    passed_metrics = sum(
        1 for result in results if result["passed"]
    )

    total_metrics = len(results)

    overall_passed = passed_metrics == total_metrics

    decision_result = get_answer_decision(results)

    return {
        "test_case_id": test_case.id,
        "question": test_case.question,
        "expected_answer": test_case.expected_answer,
        "actual_output": actual_output,
        "metrics": results,
        "passed_metrics": passed_metrics,
        "total_metrics": total_metrics,
        "overall_passed": overall_passed,
        "company_decision": decision_result["decision"],
        "decision_reason": decision_result["reason"]
    }


def run_evaluation():

    dataset = load_evaluation_dataset()
    provider = MockLLMProvider()

    evaluation_results = []

    for test_case in dataset:

        actual_output = provider.generate_response(
            test_case.question
        )

        result = evaluate_test_case(
            test_case,
            actual_output
        )

        evaluation_results.append(result)

    total_cases = len(evaluation_results)

    passed_cases = sum(
        1 for result in evaluation_results
        if result["overall_passed"]
    )

    failed_cases = total_cases - passed_cases

    pass_rate = (
        round((passed_cases / total_cases) * 100, 2)
        if total_cases > 0 else 0
    )

    accepted_cases = sum(
        1 for result in evaluation_results
        if result["company_decision"] == "ACCEPT"
    )

    review_cases = sum(
        1 for result in evaluation_results
        if result["company_decision"] == "REVIEW"
    )

    rejected_cases = sum(
        1 for result in evaluation_results
        if result["company_decision"] == "REJECT"
    )

    # Overall company decision for the entire evaluation run
    if rejected_cases > 0:
        company_decision = "REJECT"
        company_reason = (
            "One or more answers failed critical quality checks."
        )

    elif review_cases > 0:
        company_decision = "REVIEW"
        company_reason = (
            "Some answers require additional quality review."
        )

    else:
        company_decision = "ACCEPT"
        company_reason = (
            "All generated answers passed the configured checks."
        )

    return {
        "total_test_cases": total_cases,
        "passed_test_cases": passed_cases,
        "failed_test_cases": failed_cases,
        "pass_rate": pass_rate,

        "company_decision": company_decision,
        "company_decision_reason": company_reason,

        "accepted_cases": accepted_cases,
        "review_cases": review_cases,
        "rejected_cases": rejected_cases,

        "results": evaluation_results
    }
