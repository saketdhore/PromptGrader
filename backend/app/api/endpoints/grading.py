from backend.app.core.graders import master_grader
from fastapi import APIRouter, HTTPException
import logging
from app.schemas.requestSchemas import PromptRequest
from app.schemas.responseSchemas import GradeReportResponse, MasterGradeReportResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/grade", tags=["grading"], response_model=MasterGradeReportResponse, status_code=200)
async def grade_prompt(request: PromptRequest):
    try:
        logger.info(f"Received prompt for grading: {request.prompt[0:50]}...")  # Log first 50 characters for brevity

        # Call master grader
        response = master_grader.master_grade(request)
        return response

    except ValueError as ve:
        logger.error(f"Error processing prompt: {ve}")
        raise HTTPException(
            status_code=422,
            detail=f"Invalid response from the LLM: {ve}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
