from app.core.graders.master_grader import MasterGrader
from app.dependencies.openai_client import get_openai_client
from app.core.instructions.grader_instructions import MASTER_GRADER_SYSTEM_INSTRUCTIONS

master_grader = MasterGrader(
    name="Master Grader",
    system_instructions=MASTER_GRADER_SYSTEM_INSTRUCTIONS,
    openai_client=get_openai_client()
)

def get_master_grader() -> MasterGrader:
    return master_grader
