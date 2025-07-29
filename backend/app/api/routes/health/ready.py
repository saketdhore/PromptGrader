from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.dependencies.openai_client import get_openai_client

router = APIRouter()

@router.get("/readyz", tags=["Health"])
async def readiness_probe(openai = Depends(get_openai_client)):
    openai_ok = await openai.is_alive()
    if openai_ok:
        return {"status": "ready", "openai": openai_ok}

    return JSONResponse(
        status_code=503,
        content={"status": "not ready", "openai": openai_ok}
    )
