import logging
from app.schemas.request_schemas import RefinePromptRequest, PromptRequest
from app.schemas.response_schemas import PromptResponse
from app.exceptions.errors import OpenAIServiceError, PromptValidationError

logger = logging.getLogger(__name__)

class Refiner:
    def __init__(self, name: str, system_instructions: str, openai_client):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client

    async def is_alive(self):
        try:
            await self.llm_client.list_models()
            return True
        except Exception:
            return False

    async def refine(self, refine_request: RefinePromptRequest) -> PromptResponse:
        try:
            logger.info(f"[{self.name}] Refining prompt: {refine_request.original_prompt.prompt[0:50]}...")

            refiner_prompt = self._build_master_prompt(refine_request)
            refined_prompt = await self.llm_client.refine_prompt(
                prompt=refiner_prompt,
                system_instructions=self.system_instructions
            )

            logger.info(f"[{self.name}] Refining completed successfully.")
            return refined_prompt

        except PromptValidationError as ve:
            logger.warning(f"[{self.name}] Validation error during refining: {ve}")
            raise ve

        except OpenAIServiceError as oe:
            logger.error(f"[{self.name}] OpenAI service error during refining: {oe}")
            raise oe

        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error during refining: {e}")
            raise OpenAIServiceError(f"Unexpected error in Refiner: {e}") from e

    def _build_master_prompt(self, refine_request: RefinePromptRequest) -> PromptRequest:
        combined_prompt = (
            f"Original Prompt:\n"
            f"{refine_request.original_prompt.prompt.strip()}\n\n"
            f"User Instructions:\n"
            f"{refine_request.user_prompt.prompt.strip()}\n\n"
        )

        return PromptRequest(
            prompt=combined_prompt,
            tags=refine_request.original_prompt.tags
        )
