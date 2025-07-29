from fastapi import Request
from app.core.graders.master_grader import MasterGrader
from app.dependencies.openai_client import get_openai_client

def get_master_grader(request: Request) -> MasterGrader:
    return MasterGrader(
        name="Master Grader",
        system_instructions=request.app.state.system_instructions["grader"]["master"],
        assistant_instructions=request.app.state.system_instructions["grader"],
        openai_client=get_openai_client()
    )
