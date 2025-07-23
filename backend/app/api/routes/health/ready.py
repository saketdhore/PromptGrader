from fastapi import status
from fastapi.responses import JSONResponse
from app.dependencies.openai_client import get_openai_client
from fastapi import APIRouter
router = APIRouter()

@router.get("/readyz", tags=["Health"])
async def readiness_probe():
    openai_ok = await get_openai_client().is_alive()
    # Add others as needed

    if openai_ok:
        return {"status": "ready", "openai": openai_ok}

    return JSONResponse(
        status_code=503,
        content={"status": "not ready", "openai": openai_ok}
    )

