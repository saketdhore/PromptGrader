import logging
from app.schemas.request_schemas import RefinePromptRequest, PromptRequest
from app.schemas.response_schemas import PromptResponse
logger = logging.getLogger(__name__)

class Refiner:
    def __init__(self, name: str, system_instructions: str, openai_client):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client
    async def refine(self, refine_request: RefinePromptRequest) -> PromptResponse:
        try:
            logger.info(f"[{self.name}] Refining prompt: {refine_request.original_prompt.prompt[0:50]}...")
            refiner_prompt = self._build_master_prompt(
                refine_request=refine_request,
            )
            refined_prompt = await self.llm_client.refine_prompt(
                prompt = refiner_prompt,
                system_instructions=self.system_instructions
            )
            logging.info(f"[{self.name}] Refining completed successfully.")
            return refined_prompt
        except Exception as e:
            logger.error(f"[{self.name}] Failed to refine prompt: {e}")
            raise e
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
