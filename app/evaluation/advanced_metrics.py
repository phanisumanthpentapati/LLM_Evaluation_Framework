
import re


def tokenize(text):
    """Convert text into lowercase words and numbers."""
    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def extract_numbers(text):
    """Extract numerical values from text."""
    return re.findall(r"\b\d+(?:\.\d+)?\b", text)


def compare_answer_with_context(actual_output, context):
    """Compare answer with context and detect numerical contradictions."""

    answer_words = tokenize(actual_output)
    context_words = tokenize(context)

    stop_words = {
        "the", "is", "a", "an", "of", "to",
        "and", "in", "for", "on", "are", "was",
        "were", "with", "this", "that"
    }

    answer_words -= stop_words
    context_words -= stop_words

    if not answer_words:
        return 0.0, False

    # Check whether the answer contains numbers that differ
    # from the numbers in the context.
    answer_numbers = extract_numbers(actual_output)
    context_numbers = extract_numbers(context)

    numerical_conflict = (
        bool(answer_numbers)
        and bool(context_numbers)
        and answer_numbers != context_numbers
    )

    matching_words = answer_words.intersection(context_words)

    score = len(matching_words) / len(answer_words)

    # Numerical contradiction means the answer is not faithful.
    if numerical_conflict:
        score = 0.0

    return score, numerical_conflict


def faithfulness_metric(actual_output, context):
    """Measure whether the answer is supported by the context."""

    score, numerical_conflict = compare_answer_with_context(
        actual_output,
        context
    )

    passed = score >= 0.5 and not numerical_conflict

    return {
        "metric": "Faithfulness",
        "score": round(score, 2),
        "passed": passed,
        "reason": (
            "Numerical contradiction detected."
            if numerical_conflict
            else "Measures answer-token overlap with the reference context."
        )
    }


def hallucination_metric(actual_output, context):
    """Estimate unsupported content and numerical contradictions."""

    faithfulness_score, numerical_conflict = compare_answer_with_context(
        actual_output,
        context
    )

    hallucination_score = 1.0 - faithfulness_score

    return {
        "metric": "Hallucination",
        "score": round(hallucination_score, 2),
        "passed": hallucination_score <= 0.5 and not numerical_conflict,
        "reason": (
            "Potential hallucination: numerical contradiction detected."
            if numerical_conflict
            else "Estimates unsupported answer content."
        )
    }
