from app.core.engineers.engineer import Engineer
from app.dependencies.openai_client import get_openai_client
from app.core.instructions.engineer_instructions import ENGINEER_SYSTEM_INSTRUCTIONS

engineer = Engineer(
    name="Prompt Engineer",
    system_instructions=ENGINEER_SYSTEM_INSTRUCTIONS,
    openai_client=get_openai_client()
)

def get_engineer() -> Engineer:
    return engineer
