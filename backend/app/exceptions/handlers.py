# app/exceptions/handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exceptions.errors import AppBaseException
import logging

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": "HTTP_ERROR"},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")

    clean_errors = []
    for error in exc.errors():
        if "ctx" in error and isinstance(error["ctx"].get("error"), Exception):
            error["ctx"]["error"] = str(error["ctx"]["error"])
        clean_errors.append(error)

    return JSONResponse(
        status_code=422,
        content={"detail": clean_errors, "code": "VALIDATION_ERROR"},
    )


async def app_exception_handler(request: Request, exc: AppBaseException):
    logger.error(f"{exc.code}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "code": exc.code},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred", "code": "INTERNAL_SERVER_ERROR"},
    )
