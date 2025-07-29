from app.core.refiners.refiner import Refiner
from app.dependencies.openai_client import get_openai_client
from fastapi import Request


def get_refiner(request: Request) -> Refiner:
    refiner = Refiner(
        name="Prompt Refiner",
        system_instructions=request.app.state.system_instructions["engineer"]["master"],
        openai_client=get_openai_client()
    )
    