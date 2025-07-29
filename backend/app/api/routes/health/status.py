from fastapi import Depends
from fastapi import APIRouter
from app.dependencies.openai_client import get_openai_client
from app.dependencies.grader import get_master_grader
from app.dependencies.consultant import get_master_consultant
from app.dependencies.engineer import get_engineer
from app.dependencies.refiner import get_refiner

router = APIRouter()
@router.get("/statusz", tags=["Health"])
async def status_probe(
    openai = Depends(get_openai_client),
    grader = Depends(get_master_grader),
    consultant = Depends(get_master_consultant),
    engineer = Depends(get_engineer),
    refiner = Depends(get_refiner),
):
    openai_status = await openai.is_alive()
    grader_status = await grader.is_alive()
    consultant_status = await consultant.is_alive()
    engineer_status = await engineer.is_alive()
    refiner_status = await refiner.is_alive()

    overall_ok = all([
        openai_status,
        grader_status,
        consultant_status,
        engineer_status,
        refiner_status
    ])

    return {
        "status": "ok" if overall_ok else "degraded",
        "components": {
            "openai": openai_status,
            "grader": grader_status,
            "consultant": consultant_status,
            "engineer": engineer_status,
            "refiner": refiner_status
        }
    }
