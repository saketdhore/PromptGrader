from fastapi import Request
from app.core.graders.master_grader import MasterGrader
from app.dependencies.openai_client import get_openai_client
from app.core.instructions.grader_instructions import MASTER_GRADER_SYSTEM_INSTRUCTIONS

def get_master_grader(request: Request) -> MasterGrader:
    return MasterGrader(
        name="Master Grader",
        system_instructions=MASTER_GRADER_SYSTEM_INSTRUCTIONS,
        assistant_instructions=request.app.state.system_instructions["grader"],
        openai_client=get_openai_client()
    )
