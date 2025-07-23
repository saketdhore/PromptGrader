from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request_schemas import RefinePromptRequest
from app.schemas.response_schemas import PromptResponse
from app.dependencies.refiner import get_refiner
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/refine", tags=["refining"], response_model=PromptResponse, status_code=200)
async def refine(request: RefinePromptRequest, refiner=Depends(get_refiner)) -> PromptResponse:
    try:
        logger.info(f"Received prompt for refining: {request.original_prompt.prompt[0:50]}...")
        response = await refiner.refine(request)
        return response
    except ValueError as ve:
        logger.error(f"Error processing prompt: {ve}")
        raise HTTPException(
            status_code = 422,
            detail = f"Invalid response from the LLM: {ve}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )    