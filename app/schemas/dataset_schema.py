
from pydantic import BaseModel, Field
from typing import Literal


class EvaluationTestCase(BaseModel):

    id: str = Field(
        ...,
        min_length=1
    )

    category: Literal[
        "correctness",
        "relevance",
        "groundedness",
        "safety"
    ]

    question: str = Field(
        ...,
        min_length=3
    )

    context: str

    expected_answer: str

    expected_behavior: str

    should_refuse: bool = False
