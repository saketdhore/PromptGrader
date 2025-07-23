from app.core.openai_client import OpenAIClient
from app.core.graders.master_grader import MasterGrader
from app.core.instructions.grader_instructions import MASTER_GRADER_SYSTEM_INSTRUCTIONS
import logging
from app.core.consultants.master_consultant import MasterConsultant
from app.core.instructions.consultant_instructions import MASTER_CONSULTANT_SYSTEM_INSTRUCTIONS
from app.core.engineers.engineer import Engineer
from app.core.instructions.engineer_instructions import ENGINEER_SYSTEM_INSTRUCTIONS
from app.core.refiners.refiner import Refiner
from app.core.instructions.refiner_instructions import REFINER_SYSTEM_INSTRUCTIONS
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

openai_client = OpenAIClient()
logger.info("OpenAI client instance created and ready for use.")

master_grader = MasterGrader(
    name="Master Grader",
    system_instructions=MASTER_GRADER_SYSTEM_INSTRUCTIONS,
    openai_client=openai_client
)
logger.info("Master grader instance created and ready for use.")

master_consultant = MasterConsultant(
    name="Master Consultant",
    system_instructions=MASTER_CONSULTANT_SYSTEM_INSTRUCTIONS,
    openai_client=openai_client
)
logger.info("Master consultant instance created and ready for use.")

engineer = Engineer(
    name="Prompt Engineer",
    system_instructions=ENGINEER_SYSTEM_INSTRUCTIONS,
    openai_client=openai_client
)

refiner = Refiner(
    name = "Prompt Refiner",
    system_instructions = REFINER_SYSTEM_INSTRUCTIONS,
    openai_client=openai_client
)
def get_openai_client() -> OpenAIClient:
    """
    Dependency to provide the OpenAI client instance.
    This can be used in FastAPI endpoints or other parts of the application.
    """
    return openai_client
def get_master_grader() -> MasterGrader:
    """
    Dependency to provide the master grader instance.
    This can be used in FastAPI endpoints or other parts of the application.
    """
    return master_grader

def get_master_consultant() -> MasterConsultant:
    """
    Dependency to provide the master consultant instance.
    This can be used in FastAPI endpoints or other parts of the application.
    """
    return master_consultant

def get_engineer() -> Engineer:
    """
    Dependency to provide the engineer instance.
    This can be used in FastAPI endpoints or other parts of the application.
    """
    return engineer

def get_refiner() -> Refiner:
    """
    Dependency to provide the refiner instance.
    This can be used in FastAPI endpoints or other parts of the application.
    """
    return refiner