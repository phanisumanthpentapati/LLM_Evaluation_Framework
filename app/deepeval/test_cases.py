
from deepeval.test_case import LLMTestCase

from app.evaluation.dataset_loader import load_evaluation_dataset
from app.llm.provider import MockLLMProvider


def create_deepeval_test_case(test_case, actual_output):
    """
    Convert an existing dataset test case
    into a DeepEval LLMTestCase.
    """

    return LLMTestCase(
        input=test_case.question,
        actual_output=actual_output,
        expected_output=test_case.expected_answer,
        context=[test_case.context],
        retrieval_context=[test_case.context]
    )


def load_deepeval_test_cases():
    """
    Load the existing evaluation dataset
    and convert all cases into DeepEval format.
    """

    dataset = load_evaluation_dataset()
    provider = MockLLMProvider()

    deepeval_cases = []

    for test_case in dataset:

        actual_output = provider.generate_response(
            test_case.question
        )

        deepeval_case = create_deepeval_test_case(
            test_case,
            actual_output
        )

        deepeval_cases.append(deepeval_case)

    return deepeval_cases
