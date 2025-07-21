from fastapi import APIRouter
import logging
import HTTPException
from app.schemas.requestSchemas import Prompt
from app.schemas.responseSchemas import GradeReportResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/grade", tags=["grading"], response_model=GradeReportResponse, status_code=200)
async def grade_prompt(prompt: Prompt):
    try:
        logger.info(f"Received prompt for grading: {prompt.text[0:50]}...")  # Log first 50 characters for brevity
        
        #call master grader
        
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
