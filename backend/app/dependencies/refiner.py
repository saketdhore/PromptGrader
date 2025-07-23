from app.core.refiners.refiner import Refiner
from app.dependencies.openai_client import get_openai_client
from app.core.instructions.refiner_instructions import REFINER_SYSTEM_INSTRUCTIONS

refiner = Refiner(
    name="Prompt Refiner",
    system_instructions=REFINER_SYSTEM_INSTRUCTIONS,
    openai_client=get_openai_client()
)

def get_refiner() -> Refiner:
    return refiner
