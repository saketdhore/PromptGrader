from app.dependencies.grader import get_master_grader
from app.dependencies.consultant import get_master_consultant
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import MasterConsultantReportResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/consult", tags=["consulting"], response_model=MasterConsultantReportResponse, status_code=200)
async def consult(request: PromptRequest, master_consultant=Depends(get_master_consultant), master_grader=Depends(get_master_grader)) -> MasterConsultantReportResponse:
    try:
        logger.info(f"Received prompt for consulting: {request.prompt[0:50]}...")

        # First, run grading
        master_grade_report = await master_grader.master_grade(request)

        # Then, run consulting with the grading results
        response = await master_consultant.master_consult(request, master_grade_report)
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
