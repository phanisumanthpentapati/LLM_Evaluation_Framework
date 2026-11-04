
from fastapi import FastAPI
from app.llm.provider import MockLLMProvider
from app.schemas.llm_schema import GenerateRequest, GenerateResponse

app = FastAPI(
    title="LLM Evaluation Framework",
    description="Automated AI Quality Assurance Testing Framework",
    version="1.0.0"
)

# Create the mock LLM provider
llm_provider = MockLLMProvider()


@app.get("/")
def home():
    return {
        "message": "LLM Evaluation Framework is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/project-info")
def project_info():
    return {
        "project": "AI Quality Assurance",
        "framework": "LLM Evaluation Framework",
        "technologies": [
            "Python",
            "FastAPI",
            "Pytest",
            "DeepEval"
        ]
    }


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):

    answer = llm_provider.generate_response(
        request.question
    )

    return GenerateResponse(
        question=request.question,
        answer=answer,
        provider="MockLLM",
        status="success"
    )
