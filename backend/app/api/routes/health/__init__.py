from .health import router as healthz_router
from .ready import router as readyz_router
from .status import router as statusz_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(healthz_router)
router.include_router(readyz_router)
router.include_router(statusz_router)
