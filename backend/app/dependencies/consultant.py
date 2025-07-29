from fastapi import Request
from app.core.consultants.master_consultant import MasterConsultant
from app.dependencies.openai_client import get_openai_client

def get_master_consultant(request: Request) -> MasterConsultant:
    return MasterConsultant(
        name="Master Consultant",
        system_instructions=request.app.state.system_instructions["consultant"]["master"],
        assistant_instructions=request.app.state.system_instructions["consultant"],
        openai_client=get_openai_client()
    )
