from app.dependencies.grader import get_master_grader
from app.dependencies.consultant import get_master_consultant
from app.dependencies.engineer import get_engineer
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import EngineerReportResponse
import logging
from app.dependencies.limiter import limiter
router = APIRouter()
logger = logging.getLogger(__name__)

@limiter.limit("10/minute")
@router.post("/engineer", tags=["engineering"], response_model=EngineerReportResponse, status_code=200)
async def engineer(request: PromptRequest, engineer=Depends(get_engineer), master_consultant=Depends(get_master_consultant), master_grader=Depends(get_master_grader)) -> EngineerReportResponse:
    try:
        logger.info(f"Received prompt for engineering: {request.prompt[0:50]}...")

        # First, run consulting to get the master report
        master_grade_report = await master_grader.master_grade(request)
        logger.info(f"Master grading completed: {master_grade_report.overall_feedback}")
        master_consultant_report = await master_consultant.master_consult(request, master_grade_report)
        # Then, run engineering with the original prompt
        response = await engineer.engineer(request, master_consultant_report, master_grade_report)
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