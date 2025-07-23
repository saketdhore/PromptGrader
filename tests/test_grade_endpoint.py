import pytest
from unittest.mock import AsyncMock
from app.main import app
from app.api.endpoints.grading import get_master_grader
from app.schemas.responseSchemas import MasterGradeReportResponse, GradeReportResponse
from fastapi.exceptions import ResponseValidationError

# ✅ Test 1: Successful grading
@pytest.mark.asyncio
async def test_grade_endpoint_success(async_client):
    fake_report = GradeReportResponse(score=90, reasoning="Nice.", grader="Clarity Grader")
    fake_master_response = MasterGradeReportResponse(
        grade_reports={cat: fake_report for cat in ["clarity", "specificity", "complexity", "completeness", "consistency"]},
        overall_score=90,
        overall_feedback="Solid prompt"
    )
    mock_grader = AsyncMock()
    mock_grader.master_grade.return_value = fake_master_response
    app.dependency_overrides[get_master_grader] = lambda: mock_grader

    response = await async_client.post("/api/v1/grade", json={
        "prompt": "Write a short poem about autumn.",
        "tags": ["creative", "poetry"]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] == 90
    assert "clarity" in data["grade_reports"]
    assert data["grade_reports"]["clarity"]["score"] == 90

    app.dependency_overrides = {}

# ✅ Test 2: Missing required field → should return 422
@pytest.mark.asyncio
async def test_grade_missing_prompt(async_client):
    response = await async_client.post("/api/v1/grade", json={
        "tags": ["missing prompt"]
    })
    assert response.status_code == 422

# ✅ Test 3: Simulate LLM crash → should return 500
@pytest.mark.asyncio
async def test_grade_llm_crash(async_client):
    mock_grader = AsyncMock()
    mock_grader.master_grade.side_effect = Exception("Boom")
    app.dependency_overrides[get_master_grader] = lambda: mock_grader

    response = await async_client.post("/api/v1/grade", json={
        "prompt": "Trigger crash",
        "tags": []
    })

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"

    app.dependency_overrides = {}

# ✅ Test 4: Malformed response schema → should raise ResponseValidationError
@pytest.mark.asyncio
async def test_grade_invalid_schema(async_client):
    # Fake response object with missing 'score' key (violates GradeReportResponse)
    class FakeBadResponse:
        def __init__(self):
            self.grade_reports = {
                "clarity": {"reasoning": "no score", "grader": "Grader"}  # ❌ Missing 'score'
            }
            self.overall_score = 0
            self.overall_feedback = "Oops"

    mock_grader = AsyncMock()
    mock_grader.master_grade.return_value = FakeBadResponse()
    app.dependency_overrides[get_master_grader] = lambda: mock_grader

    with pytest.raises(ResponseValidationError) as exc_info:
        await async_client.post("/api/v1/grade", json={
            "prompt": "Bad schema",
            "tags": []
        })

    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('response', 'grade_reports', 'clarity', 'score')
    assert errors[0]['msg'] == 'Field required'

    app.dependency_overrides = {}
