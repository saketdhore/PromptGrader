from app.core.consultants.master_consultant import MasterConsultant
from app.dependencies.openai_client import get_openai_client
from app.core.instructions.consultant_instructions import MASTER_CONSULTANT_SYSTEM_INSTRUCTIONS

master_consultant = MasterConsultant(
    name="Master Consultant",
    system_instructions=MASTER_CONSULTANT_SYSTEM_INSTRUCTIONS,
    openai_client=get_openai_client()
)

def get_master_consultant() -> MasterConsultant:
    return master_consultant
