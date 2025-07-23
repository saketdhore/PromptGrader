# app/api/endpoints/health.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/healthz", tags=["Health"])
async def liveness_probe():
    return JSONResponse(content={"status": "alive"}, status_code=200)
