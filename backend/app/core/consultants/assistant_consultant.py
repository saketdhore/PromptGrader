import logging
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import (
    GradeReportResponse, ConsultantReportResponse
)
from app.core.clients.openai_client import OpenAIClient
logger = logging.getLogger(__name__)
class AssistantConsultant:
    def __init__(self, name: str, system_instructions: str, openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client

    async def consult(self, prompt: PromptRequest, grade_report: GradeReportResponse) -> ConsultantReportResponse:
        try:
            logger.info(f"[{self.name}] Consulting prompt: {prompt.prompt[0:50]}...")  # Log first 50 characters for brevity
            master_prompt = self._build_master_prompt(prompt, grade_report)
            response = await self.llm_client.consult_prompt(
                prompt=master_prompt,
                system_instructions=self.system_instructions
            )
            return response  # Assuming consult_prompt returns ConsultantReportResponse
        except Exception as e:
            logger.error(f"[{self.name}] Error consulting prompt: {e}")
            raise

    def _build_master_prompt(self, prompt: PromptRequest, grade_report: GradeReportResponse) -> PromptRequest:
        refined_prompt = f"""
        # Original Prompt:
        {prompt.prompt}

        # Grading Report:
        - Score: {grade_report.score}
        - Reasoning: {grade_report.reasoning}
        """
        return PromptRequest(prompt=refined_prompt, tags=prompt.tags)
