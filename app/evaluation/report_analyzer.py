
def analyze_evaluation_report(report):

    results = report.get("results", [])

    metric_summary = {}
    failed_test_cases = []
    case_decisions = []

    for test_case in results:

        # Collect metric-wise statistics
        for metric in test_case["metrics"]:

            metric_name = metric["metric"]

            if metric_name not in metric_summary:
                metric_summary[metric_name] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0
                }

            metric_summary[metric_name]["total"] += 1

            if metric["passed"]:
                metric_summary[metric_name]["passed"] += 1
            else:
                metric_summary[metric_name]["failed"] += 1

        # Store company decision for each answer
        case_decisions.append({
            "test_case_id": test_case["test_case_id"],
            "question": test_case["question"],
            "expected_answer": test_case.get("expected_answer", ""),
            "actual_output": test_case["actual_output"],
            "decision": test_case.get("company_decision", "REVIEW"),
            "reason": test_case.get("decision_reason", "")
        })

        # Collect failed test cases
        if not test_case["overall_passed"]:

            failed_metrics = [
                {
                    "metric": metric["metric"],
                    "score": metric.get("score"),
                    "reason": metric.get(
                        "reason",
                        "No reason provided"
                    )
                }
                for metric in test_case["metrics"]
                if not metric["passed"]
            ]

            failed_test_cases.append({
                "test_case_id": test_case["test_case_id"],
                "question": test_case["question"],
                "actual_output": test_case["actual_output"],
                "failed_metrics": failed_metrics,
                "company_decision": test_case.get(
                    "company_decision",
                    "REVIEW"
                ),
                "decision_reason": test_case.get(
                    "decision_reason",
                    ""
                )
            })

    # Calculate individual metric pass rates
    for summary in metric_summary.values():

        total = summary["total"]

        summary["pass_rate"] = (
            round(summary["passed"] / total * 100, 2)
            if total else 0
        )

    return {
        "total_test_cases": report.get(
            "total_test_cases",
            len(results)
        ),

        "passed_test_cases": report.get(
            "passed_test_cases",
            0
        ),

        "failed_test_cases": report.get(
            "failed_test_cases",
            0
        ),

        "overall_pass_rate": report.get(
            "pass_rate",
            0
        ),

        "company_decision": report.get(
            "company_decision",
            "REVIEW"
        ),

        "company_decision_reason": report.get(
            "company_decision_reason",
            ""
        ),

        "accepted_cases": report.get("accepted_cases", 0),
        "review_cases": report.get("review_cases", 0),
        "rejected_cases": report.get("rejected_cases", 0),

        "case_decisions": case_decisions,

        "metric_summary": metric_summary,

        "failed_case_details": failed_test_cases
    }
