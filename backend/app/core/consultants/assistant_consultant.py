import logging
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import (
    GradeReportResponse, ConsultantReportResponse
)
from app.core.clients.openai_client import OpenAIClient
from app.exceptions.errors import OpenAIServiceError, PromptValidationError

logger = logging.getLogger(__name__)

class AssistantConsultant:
    def __init__(self, name: str, system_instructions: str, openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client

    async def consult(self, prompt: PromptRequest, grade_report: GradeReportResponse) -> ConsultantReportResponse:
        try:
            logger.info(f"[{self.name}] Consulting on prompt: {prompt.prompt[0:50]}...")  # Truncate for log clarity
            master_prompt = self._build_master_prompt(prompt, grade_report)

            response = await self.llm_client.consult_prompt(
                prompt=master_prompt,
                system_instructions=self.system_instructions
            )

            logger.info(f"[{self.name}] Consultation completed.")
            return response

        except PromptValidationError as ve:
            logger.warning(f"[{self.name}] Prompt validation failed: {ve}")
            raise ve

        except OpenAIServiceError as oe:
            logger.error(f"[{self.name}] OpenAI service failure: {oe}")
            raise oe

        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error during consultation: {e}")
            raise OpenAIServiceError(f"Unexpected error in AssistantConsultant: {e}") from e

    def _build_master_prompt(self, prompt: PromptRequest, grade_report: GradeReportResponse) -> PromptRequest:
        refined_prompt = f"""
        # Original Prompt:
        {prompt.prompt}

        # Grading Report:
        - Score: {grade_report.score}
        - Reasoning: {grade_report.reasoning}
        """
        return PromptRequest(prompt=refined_prompt, tags=prompt.tags)
