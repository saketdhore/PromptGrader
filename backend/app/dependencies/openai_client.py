import logging
from app.core.clients.openai_client import OpenAIClient
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

openai_client = OpenAIClient()
logger.info("OpenAI client instance created and ready for use.")

def get_openai_client() -> OpenAIClient:
    return openai_client