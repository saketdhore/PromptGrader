import pytest
from unittest.mock import AsyncMock
from fastapi.exceptions import ResponseValidationError
from app.main import app
from app.api.endpoints.engineering import get_master_grader, get_master_consultant, get_engineer
from app.schemas.responseSchemas import (
    MasterGradeReportResponse,
    MasterConsultantReportResponse,
    EngineerReportResponse,
    GradeReportResponse,
    ConsultantReportResponse
)

# ✅ Test 1: Successful engineer flow
@pytest.mark.asyncio
async def test_engineer_endpoint_success(async_client):
    # Fake grading and consulting responses
    fake_grade = GradeReportResponse(score=90, reasoning="Good", grader="Grader")
    fake_master_grade = MasterGradeReportResponse(
        grade_reports={cat: fake_grade for cat in ["clarity", "specificity", "complexity", "completeness", "consistency"]},
        overall_score=90,
        overall_feedback="Well written"
    )

    fake_consult = ConsultantReportResponse(suggestion="Refine it", consultant="Consultant")
    fake_master_consult = MasterConsultantReportResponse(
        consultant_reports={cat: fake_consult for cat in ["clarity", "specificity", "complexity", "completeness", "consistency"]},
        overall_suggestion="Improve clarity"
    )

    fake_engineer_response = EngineerReportResponse(
        original_prompt={"prompt": "Test prompt", "tags": ["example"]},
        refined_prompt={"prompt": "Better prompt", "tags": ["example"]}
    )

    # Inject mocks
    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_engineer = AsyncMock()

    mock_grader.master_grade.return_value = fake_master_grade
    mock_consultant.master_consult.return_value = fake_master_consult
    mock_engineer.engineer.return_value = fake_engineer_response

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant
    app.dependency_overrides[get_engineer] = lambda: mock_engineer

    response = await async_client.post("/api/v1/engineer", json={
        "prompt": "Test prompt",
        "tags": ["example"]
    })

    assert response.status_code == 200
    data = response.json()
    assert "original_prompt" in data and "refined_prompt" in data
    assert data["refined_prompt"]["prompt"] == "Better prompt"
    assert data["refined_prompt"]["tags"] == ["example"]

    app.dependency_overrides = {}

# ✅ Test 2: Missing prompt → 422
@pytest.mark.asyncio
async def test_engineer_missing_prompt(async_client):
    response = await async_client.post("/api/v1/engineer", json={"tags": ["missing"]})
    assert response.status_code == 422

# ✅ Test 3: Grader crashes → 500
@pytest.mark.asyncio
async def test_engineer_grader_crash(async_client):
    mock_grader = AsyncMock()
    mock_grader.master_grade.side_effect = Exception("Grader failed")
    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: AsyncMock()
    app.dependency_overrides[get_engineer] = lambda: AsyncMock()

    response = await async_client.post("/api/v1/engineer", json={
        "prompt": "Trigger error",
        "tags": []
    })

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"
    app.dependency_overrides = {}

# ✅ Test 4: Consultant crashes → 500
@pytest.mark.asyncio
async def test_engineer_consultant_crash(async_client):
    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_grader.master_grade.return_value = MasterGradeReportResponse(
        grade_reports={}, overall_score=0, overall_feedback="temp"
    )
    mock_consultant.master_consult.side_effect = Exception("Consulting failed")

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant
    app.dependency_overrides[get_engineer] = lambda: AsyncMock()

    response = await async_client.post("/api/v1/engineer", json={
        "prompt": "Trigger error",
        "tags": []
    })

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"
    app.dependency_overrides = {}

# ✅ Test 5: Engineer crashes → 500
@pytest.mark.asyncio
async def test_engineer_crash(async_client):
    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_engineer = AsyncMock()

    mock_grader.master_grade.return_value = MasterGradeReportResponse(
        grade_reports={}, overall_score=0, overall_feedback="temp"
    )
    mock_consultant.master_consult.return_value = MasterConsultantReportResponse(
        consultant_reports={}, overall_suggestion="temp"
    )
    mock_engineer.engineer.side_effect = Exception("Engineer broke")

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant
    app.dependency_overrides[get_engineer] = lambda: mock_engineer

    response = await async_client.post("/api/v1/engineer", json={
        "prompt": "Trigger error",
        "tags": []
    })

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"
    app.dependency_overrides = {}

# ✅ Test 6: Malformed engineer response → raises ResponseValidationError
@pytest.mark.asyncio
async def test_engineer_invalid_schema(async_client):
    # Return dict instead of EngineerReportResponse-compatible object
    class FakeBadEngineerResponse:
        def __init__(self):
            self.original_prompt = {"prompt": "ok", "tags": "not-a-list"}  # ❌ tags should be a list
            self.refined_prompt = {"prompt": "better", "tags": "also-not-a-list"}

    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_engineer = AsyncMock()

    mock_grader.master_grade.return_value = MasterGradeReportResponse(
        grade_reports={}, overall_score=0, overall_feedback="temp"
    )
    mock_consultant.master_consult.return_value = MasterConsultantReportResponse(
        consultant_reports={}, overall_suggestion="temp"
    )
    mock_engineer.engineer.return_value = FakeBadEngineerResponse()

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant
    app.dependency_overrides[get_engineer] = lambda: mock_engineer

    with pytest.raises(ResponseValidationError) as exc_info:
        await async_client.post("/api/v1/engineer", json={
            "prompt": "Bad output format",
            "tags": []
        })
    errors = exc_info.value.errors()
    assert errors[0]["loc"][-1] == "tags"
    assert "valid list" in errors[0]["msg"]
    app.dependency_overrides = {}
