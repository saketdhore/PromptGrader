import logging
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import GradeReportResponse
from app.core.clients.openai_client import OpenAIClient
from app.exceptions.errors import OpenAIServiceError, PromptValidationError

logger = logging.getLogger(__name__)

class AssistantGrader:
    def __init__(self, name: str, system_instructions: str, openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client

    async def grade(self, prompt: PromptRequest) -> GradeReportResponse:
        try:
            logger.info(f"[{self.name}] Grading prompt: {prompt.prompt[0:50]}...")
            return await self.llm_client.grade_prompt(prompt, self.system_instructions)

        except PromptValidationError as ve:
            logger.warning(f"[{self.name}] Prompt validation failed: {ve}")
            raise ve

        except OpenAIServiceError as oe:
            logger.error(f"[{self.name}] OpenAI service error: {oe}")
            raise oe

        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error during grading: {e}")
            raise OpenAIServiceError(f"Unexpected error in AssistantGrader: {e}") from e