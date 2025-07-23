from app.api.routes.grading.router import router as grading_router
from app.api.routes.consulting.router import router as consulting_router
from app.api.routes.engineering.router import router as engineering_router
from app.api.routes.refining.router import router as refining_router
from app.api.routes.health import router as health_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    app_exception_handler,
    generic_exception_handler
)
from app.exceptions.errors import AppBaseException

from fastapi import FastAPI
import logging
import uvicorn
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PromptScore API",
    description="API for grading and refining prompts",
    version="1.0.0",
)

# 🚀 Include routers
app.include_router(grading_router, prefix="/api/v1", tags=["grading"])
app.include_router(consulting_router, prefix="/api/v1", tags=["consulting"])
app.include_router(engineering_router, prefix="/api/v1", tags=["engineering"])
app.include_router(refining_router, prefix="/api/v1", tags=["refining"])
app.include_router(health_router, prefix="/api/v1", tags=["Health"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Prompt Scorer API!"}

if __name__ == "__main__":
    logger.info("Loading environment variables...")
    load_dotenv()
    logger.info("Environment variables loaded successfully.")
    logger.info("Starting FastAPI application...")
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    app.add_exception_handler(AppBaseException, app_exception_handler)
    uvicorn.run(app, host="0.0.0.0", port=8000)
