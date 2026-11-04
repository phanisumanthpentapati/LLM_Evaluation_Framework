
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Question provided to the LLM"
    )


class GenerateResponse(BaseModel):
    question: str
    answer: str
    provider: str
    status: str
