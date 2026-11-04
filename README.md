# LLM Evaluation Framework

An automated framework for evaluating, testing, and monitoring Large Language Model (LLM) responses using Python, FastAPI, Pytest, and evaluation metrics.

The framework helps assess the quality of AI-generated responses through automated test cases, metric-based evaluation, quality decisions, and a visual evaluation dashboard.

---

## Project Overview

Large Language Models can generate responses that are incorrect, irrelevant, misleading, or unsafe. Therefore, evaluating their responses is important before integrating them into real-world applications.

The **LLM Evaluation Framework** provides an automated approach to test and evaluate LLM responses against predefined datasets and expected outputs.

It evaluates responses using multiple quality metrics and generates reports to help identify failures and assess overall response quality.

## Key Features

- **Automated Evaluation:** Execute multiple LLM evaluation test cases automatically.
- **Multiple Evaluation Metrics:** Evaluate correctness, relevance, groundedness, safety, faithfulness, and hallucination-related indicators.
- **Dataset-Based Testing:** Load and validate evaluation datasets from JSON files.
- **FastAPI Backend:** Expose REST APIs to generate responses and execute evaluations.
- **Visual Evaluation Dashboard:** Monitor evaluation results through an interactive dashboard.
- **Company-Level Quality Decisions:** Classify test cases into ACCEPT, REVIEW, and REJECT categories.
- **Evaluation Reports:** Generate JSON reports containing detailed test results.
- **Automated Testing:** Use Pytest to validate application functionality.
- **Extensible Architecture:** Support future integration of real LLM providers and advanced evaluation methods.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.11 |
| Backend Framework | FastAPI |
| Data Validation | Pydantic |
| Testing Framework | Pytest |
| API Testing | HTTPX |
| LLM Evaluation Library | DeepEval (installed; advanced LLM-as-a-judge integration planned) |
| Dataset Format | JSON |
| Frontend | HTML, CSS, JavaScript |
| Visualization | Chart.js |
| Server | Uvicorn |
| Version Control | Git and GitHub |
| CI/CD | GitHub Actions (planned) |

## Project Architecture

```text
llm-evaluation-framework/
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── provider.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── llm_schema.py
│   │   └── dataset_schema.py
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── dataset_loader.py
│   │   ├── metrics.py
│   │   ├── evaluator.py
│   │   ├── report_writer.py
│   │   ├── advanced_metrics.py
│   │   └── report_analyzer.py
│   │
│   ├── deepeval/
│   │   ├── __init__.py
│   │   ├── test_cases.py
│   │   └── metrics.py
│   │
│   └── static/
│       └── index.html
│
├── datasets/
│   └── evaluation_dataset.json
│
├── reports/
│
├── tests/
│   ├── test_api.py
│   ├── test_dataset.py
│   ├── test_evaluator.py
│   ├── test_report_writer.py
│   ├── test_deepeval_metrics.py
│   ├── test_advanced_metrics.py
│   └── test_report_analyzer.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The architecture above reflects the intended project structure. Include the GitHub Actions workflow only after creating it.*

## Evaluation Metrics

The framework currently implements seven evaluation indicators.

| Metric | Description |
|---|---|
| Correctness | Compares the generated response with the expected answer. |
| Relevance | Checks whether the response addresses the question. |
| Groundedness | Checks response support through available context and keyword overlap. |
| Safety | Checks for unsafe responses and refusal behavior using predefined rules. |
| Answer Relevancy | Measures keyword-based relevance between the question and generated answer. |
| Faithfulness | Uses rule-based context and token comparisons to estimate support. |
| Hallucination | Uses heuristic checks, including numerical inconsistencies and context overlap. |

**Note:** The current implementation uses a mock LLM provider and primarily rule-based evaluation methods. These metrics are initial approximations, not comprehensive semantic evaluations. DeepEval is installed, but a real LLM-as-a-judge integration is a planned enhancement.

## Quality Decision System

Each test case receives a quality decision based on the configured evaluation rules.

| Decision | Meaning |
|---|---|
| ACCEPT | All configured evaluation metrics pass. |
| REVIEW | Only non-critical metrics fail. |
| REJECT | At least one critical metric fails. |

The framework considers correctness, safety, groundedness, faithfulness, and hallucination indicators as critical metrics.

The overall evaluation run also produces ACCEPT, REVIEW, or REJECT based on the individual test-case decisions.

These decisions are demonstration quality gates based on the current heuristic metrics, not guarantees of factual correctness.

## Dashboard

The interactive dashboard provides a visual overview of evaluation results.

Features include:

- Total test cases
- Passed and failed test cases
- Overall pass percentage
- Individual metric performance
- Company-level quality decisions
- Accepted, review, and rejected test cases
- Individual test-case inspection
- Expected answer versus actual output
- Failed test-case details

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/llm-evaluation-framework.git
```

```bash
cd llm-evaluation-framework
```

Replace `YOUR_USERNAME` with your GitHub username after creating the repository.

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The application will start at:

```text
http://127.0.0.1:8000
```

## Application URLs

| Resource | URL |
|---|---|
| Main API | http://127.0.0.1:8000/ |
| Health Check | http://127.0.0.1:8000/health |
| Project Information | http://127.0.0.1:8000/project-info |
| Swagger API Documentation | http://127.0.0.1:8000/docs |
| Evaluation Dashboard | http://127.0.0.1:8000/dashboard/ |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application welcome endpoint |
| GET | `/health` | Check application health |
| GET | `/project-info` | Retrieve project information |
| POST | `/generate` | Generate a response using the configured provider |
| GET | `/evaluation/dataset` | Retrieve evaluation dataset information |
| GET | `/evaluation/summary` | Retrieve evaluation summary |
| POST | `/evaluation/run` | Execute evaluation test cases |
| POST | `/evaluation/analyze` | Execute evaluation and generate analysis |

For request and response schemas, visit the Swagger documentation at `/docs`.

## Running Automated Tests

Execute the complete test suite:

```bash
python -m pytest -v
```

Run a specific test file:

```bash
python -m pytest tests/test_evaluator.py -v
```

Run tests with a summary:

```bash
python -m pytest -v --tb=short
```

## Evaluation Workflow

1. Load evaluation test cases from the JSON dataset.
2. Validate the dataset using Pydantic schemas.
3. Send questions to the configured LLM provider.
4. Collect generated responses.
5. Evaluate responses using the configured metrics.
6. Calculate individual test-case results.
7. Apply ACCEPT, REVIEW, or REJECT quality decisions.
8. Analyze the evaluation results.
9. Save evaluation reports in JSON format.
10. Display results on the interactive dashboard.

## Sample Dataset Format

The evaluation dataset contains predefined questions, expected answers, and supporting information.

Example:

```json
{
  "id": "TC001",
  "question": "What is the capital of India?",
  "expected_answer": "The capital of India is New Delhi.",
  "context": "New Delhi is the capital of India."
}
```

Refer to `datasets/evaluation_dataset.json` for the actual dataset structure used by the application.

## Sample Evaluation Report

An evaluation report contains information such as:

- Test case ID
- Question
- Expected answer
- Actual generated output
- Individual metric scores
- Passed and failed metrics
- Overall test-case result
- Company-level quality decision
- Evaluation timestamp

Reports are stored in the `reports/` directory.

## Current Limitations

- The current LLM provider uses predefined mock responses rather than a real language model.
- Several evaluation metrics use keyword matching and rule-based heuristics.
- DeepEval is installed, but semantic LLM-as-a-judge evaluation is not yet integrated.
- The current dataset contains a limited number of test cases.
- The quality decisions are based on configured demonstration rules.

## Future Enhancements

- Integrate real LLM providers such as OpenAI or other supported models.
- Implement DeepEval-based LLM-as-a-judge evaluation.
- Add semantic similarity and embedding-based evaluation.
- Introduce prompt testing and prompt version comparison.
- Expand datasets with adversarial and edge-case test scenarios.
- Add regression testing for prompt and model changes.
- Implement automated CI/CD using GitHub Actions.
- Add evaluation history and model performance comparisons.
- Support evaluation of multiple LLM providers.

## Learning Outcomes

This project demonstrates practical knowledge of:

- Large Language Model testing and evaluation
- Python backend development
- REST API development using FastAPI
- Automated testing using Pytest
- Dataset validation using Pydantic
- Evaluation metrics and quality gates
- JSON-based reporting
- Dashboard development
- AI quality assurance concepts


