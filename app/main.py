
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.llm.provider import MockLLMProvider
from app.schemas.llm_schema import GenerateRequest, GenerateResponse

from app.evaluation.dataset_loader import (
    load_evaluation_dataset,
    get_dataset_summary
)

from app.evaluation.evaluator import run_evaluation
from app.evaluation.report_writer import save_evaluation_report
from app.evaluation.report_analyzer import analyze_evaluation_report


# Initialize FastAPI application
app = FastAPI(
    title="LLM Evaluation Framework",
    description="Automated testing and evaluation framework for LLM applications",
    version="1.0.0"
)


# Initialize mock LLM provider
llm_provider = MockLLMProvider()


# Configure dashboard static files
STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount(
    "/dashboard",
    StaticFiles(directory=STATIC_DIR, html=True),
    name="dashboard"
)


# --------------------------------------------------
# HOME API
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "LLM Evaluation Framework is running",
        "status": "success"
    }


# --------------------------------------------------
# HEALTH CHECK API
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# PROJECT INFORMATION API
# --------------------------------------------------

@app.get("/project-info")
def project_info():
    return {
        "project": "LLM Evaluation Framework",
        "technologies": [
            "Python",
            "FastAPI",
            "Pytest",
            "DeepEval",
            "Pydantic",
            "HTTPX"
        ]
    }


# --------------------------------------------------
# GENERATE ANSWER API
# --------------------------------------------------

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


# --------------------------------------------------
# GET EVALUATION DATASET API
# --------------------------------------------------

@app.get("/evaluation/dataset")
def get_evaluation_dataset():

    dataset = load_evaluation_dataset()

    return [
        test_case.model_dump()
        for test_case in dataset
    ]


# --------------------------------------------------
# EVALUATION DATASET SUMMARY API
# --------------------------------------------------

@app.get("/evaluation/summary")
def evaluation_summary():

    return get_dataset_summary()


# --------------------------------------------------
# RUN EVALUATION API
# --------------------------------------------------

@app.post("/evaluation/run")
def run_full_evaluation():

    report = run_evaluation()

    report_path = save_evaluation_report(report)

    return {
        "message": "Evaluation completed successfully",
        "report_saved": True,
        "report_path": report_path,
        "evaluation_report": report
    }


# --------------------------------------------------
# DETAILED EVALUATION ANALYSIS API
# --------------------------------------------------

@app.post("/evaluation/analyze")
def analyze_full_evaluation():

    # Execute all evaluation metrics
    report = run_evaluation()

    # Analyze evaluation results
    analysis = analyze_evaluation_report(report)

    # Save evaluation report
    report_path = save_evaluation_report(report)

    return {
        "message": "Evaluation analysis completed successfully",
        "report_saved": True,
        "report_path": report_path,
        "analysis": analysis
    }
