import pytest
from unittest.mock import AsyncMock
from app.main import app
from app.api.endpoints.consulting import get_master_grader, get_master_consultant
from app.schemas.response_schemas import (
    MasterConsultantReportResponse,
    ConsultantReportResponse,
    MasterGradeReportResponse,
    GradeReportResponse,
)
from fastapi.exceptions import ResponseValidationError

# ✅ Test 1: Successful consulting
@pytest.mark.asyncio
async def test_consult_endpoint_success(async_client):
    # Fake grading and consulting responses
    fake_grade_report = GradeReportResponse(score=90, reasoning="Nice.", grader="Clarity Grader")
    fake_master_grade_response = MasterGradeReportResponse(
        grade_reports={cat: fake_grade_report for cat in ["clarity", "specificity", "complexity", "completeness", "consistency"]},
        overall_score=90,
        overall_feedback="Solid prompt"
    )

    fake_consult_report = ConsultantReportResponse(suggestion="Make it more specific", consultant="Clarity Consultant")
    fake_master_consult_response = MasterConsultantReportResponse(
        consultant_reports={cat: fake_consult_report for cat in ["clarity", "specificity", "complexity", "completeness", "consistency"]},
        overall_suggestion="Be more specific overall"
    )

    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_grader.master_grade.return_value = fake_master_grade_response
    mock_consultant.master_consult.return_value = fake_master_consult_response

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant

    response = await async_client.post("/api/v1/consult", json={
        "prompt": "What are the sales trends?",
        "tags": []
    })

    assert response.status_code == 200
    data = response.json()
    assert "overall_suggestion" in data
    assert data["overall_suggestion"] == "Be more specific overall"
    assert "clarity" in data["consultant_reports"]
    assert data["consultant_reports"]["clarity"]["suggestion"] == "Make it more specific"

    app.dependency_overrides = {}

# ✅ Test 2: Missing prompt field → 422
@pytest.mark.asyncio
async def test_consult_missing_prompt(async_client):
    response = await async_client.post("/api/v1/consult", json={
        "tags": ["oops"]
    })
    assert response.status_code == 422

# ✅ Test 3: Simulate grader crash → 500
@pytest.mark.asyncio
async def test_consult_grader_crash(async_client):
    mock_grader = AsyncMock()
    mock_grader.master_grade.side_effect = Exception("Boom in grading")
    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: AsyncMock()

    response = await async_client.post("/api/v1/consult", json={
        "prompt": "Trigger crash",
        "tags": []
    })

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"
    app.dependency_overrides = {}

# ✅ Test 4: Simulate consultant crash → 500
@pytest.mark.asyncio
async def test_consult_consultant_crash(async_client):
    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_grader.master_grade.return_value = MasterGradeReportResponse(
        grade_reports={}, overall_score=0, overall_feedback="Placeholder"
    )
    mock_consultant.master_consult.side_effect = Exception("Boom in consulting")

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant

    response = await async_client.post("/api/v1/consult", json={
        "prompt": "Trigger crash",
        "tags": []
    })

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"
    app.dependency_overrides = {}

# ✅ Test 5: Consultant returns malformed data → should raise validation error
@pytest.mark.asyncio
async def test_consult_invalid_schema(async_client):
    class FakeBadResponse:
        def __init__(self):
            self.consultant_reports = {
                "clarity": {"consultant": "Consultant Name"}  # ❌ Missing 'suggestion'
            }
            self.overall_suggestion = "Missing suggestion in clarity"

    mock_grader = AsyncMock()
    mock_consultant = AsyncMock()
    mock_grader.master_grade.return_value = MasterGradeReportResponse(
        grade_reports={}, overall_score=0, overall_feedback="Placeholder"
    )
    mock_consultant.master_consult.return_value = FakeBadResponse()

    app.dependency_overrides[get_master_grader] = lambda: mock_grader
    app.dependency_overrides[get_master_consultant] = lambda: mock_consultant

    with pytest.raises(ResponseValidationError) as exc_info:
        await async_client.post("/api/v1/consult", json={
            "prompt": "Schema bug",
            "tags": []
        })

    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('response', 'consultant_reports', 'clarity', 'suggestion')
    assert errors[0]['msg'] == 'Field required'

    app.dependency_overrides = {}
