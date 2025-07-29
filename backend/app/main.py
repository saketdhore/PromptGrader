from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import logging
import uvicorn

from app.api.routes.grading.router import router as grading_router
from app.api.routes.consulting.router import router as consulting_router
from app.api.routes.engineering.router import router as engineering_router
from app.api.routes.refining.router import router as refining_router
from app.api.routes.health import router as health_router
from app.dependencies.limiter import limiter
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    app_exception_handler,
    generic_exception_handler,
)
from app.exceptions.errors import AppBaseException
from app.db.session import SessionLocal
from app.db.models.system_instructions import SystemInstructions


# 🚀 Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ✅ Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    try:
        instructions = db.query(SystemInstructions).all()

        # Build: system_instructions[role][type] = content
        cached_instructions = {}
        for inst in instructions:
            if inst.role not in cached_instructions:
                cached_instructions[inst.role] = {}
            cached_instructions[inst.role][inst.type] = inst.instructions

        app.state.system_instructions = cached_instructions
        print("✅ System instructions loaded into memory")
        yield
    finally:
        db.close()
        print("🧹 DB session closed")

# ✅ App instance
app = FastAPI(
    title="PromptScore API",
    description="API for grading and refining prompts",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter

# ✅ Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(AppBaseException, app_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ✅ Register routers
app.include_router(grading_router, prefix="/api/v1", tags=["grading"])
app.include_router(consulting_router, prefix="/api/v1", tags=["consulting"])
app.include_router(engineering_router, prefix="/api/v1", tags=["engineering"])
app.include_router(refining_router, prefix="/api/v1", tags=["refining"])
app.include_router(health_router, prefix="/api/v1", tags=["Health"])

# ✅ Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Prompt Scorer API!"}

# ✅ App entry point
if __name__ == "__main__":
    logger.info("Loading environment variables...")
    load_dotenv()
    logger.info("Environment variables loaded successfully.")
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
