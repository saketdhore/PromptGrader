from app.core.engineers.engineer import Engineer
from app.dependencies.openai_client import get_openai_client
from fastapi import Request

def get_engineer(request: Request) -> Engineer:
    engineer = Engineer(
    name="Prompt Engineer",
    system_instructions=request.app.state.system_instructions["engineer"]["master"],
    openai_client=get_openai_client()
    )
    return engineer
