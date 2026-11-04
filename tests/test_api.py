
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_api():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_health_api():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_project_info_api():
    response = client.get("/project-info")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "AI Quality Assurance"
    assert "FastAPI" in data["technologies"]

def test_generate_return_policy():
    response = client.post(
        "/generate",
        json={"question": "What is the return policy?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["provider"] == "MockLLM"
    assert data["status"] == "success"
    assert "10 days" in data["answer"]


def test_generate_python_answer():
    response = client.post(
        "/generate",
        json={"question": "What is Python?"}
    )

    assert response.status_code == 200
    assert "programming language" in response.json()["answer"]


def test_generate_invalid_question():
    response = client.post(
        "/generate",
        json={"question": "Hi"}
    )

    assert response.status_code == 422
