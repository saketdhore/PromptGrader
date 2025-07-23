import pytest
from unittest.mock import AsyncMock
from fastapi.exceptions import ResponseValidationError
from app.main import app
from app.dependencies import get_refiner
from app.schemas.request_schemas import RefinePromptRequest, PromptRequest


@pytest.mark.asyncio
async def test_refine_endpoint_success(async_client):
    mock_response = PromptRequest(prompt="Refined prompt.", tags=["refined"])

    mock_refiner = AsyncMock()
    mock_refiner.refine.return_value = mock_response
    app.dependency_overrides[get_refiner] = lambda: mock_refiner

    payload = {
        "original_prompt": {"prompt": "Original prompt", "tags": ["original"]},
        "user_prompt": {"prompt": "Make it better", "tags": ["suggestion"]}
    }

    response = await async_client.post("/api/v1/refine", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == "Refined prompt."
    assert data["tags"] == ["refined"]

    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_refine_missing_required_field(async_client):
    # Missing `original_prompt`
    response = await async_client.post("/api/v1/refine", json={
        "user_prompt": {"prompt": "Add detail", "tags": ["idea"]}
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_refine_llm_crash(async_client):
    mock_refiner = AsyncMock()
    mock_refiner.refine.side_effect = Exception("Something went wrong")
    app.dependency_overrides[get_refiner] = lambda: mock_refiner

    payload = {
        "original_prompt": {"prompt": "Original prompt", "tags": ["test"]},
        "user_prompt": {"prompt": "Add more clarity", "tags": ["test"]}
    }

    response = await async_client.post("/api/v1/refine", json=payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred"

    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_refine_invalid_schema(async_client):
    # Returns wrong type for `tags`
    class BadRefineResponse:
        def __init__(self):
            self.prompt = "Broken prompt"
            self.tags = "notalist"  # ❌ should be a list

    mock_refiner = AsyncMock()
    mock_refiner.refine.return_value = BadRefineResponse()
    app.dependency_overrides[get_refiner] = lambda: mock_refiner

    with pytest.raises(ResponseValidationError):
        await async_client.post("/api/v1/refine", json={
            "original_prompt": {"prompt": "fix", "tags": ["x"]},
            "user_prompt": {"prompt": "shorter", "tags": ["y"]}
        })

    app.dependency_overrides = {}
