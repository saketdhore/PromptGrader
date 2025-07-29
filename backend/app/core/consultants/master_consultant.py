import logging
import asyncio
from typing import Dict
from app.core.clients.openai_client import OpenAIClient
from app.core.consultants.assistant_consultant import AssistantConsultant
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import (
    MasterConsultantReportResponse,
    ConsultantReportResponse,
    MasterGradeReportResponse,
    OverallSuggestionResponse
)
from app.exceptions.errors import OpenAIServiceError, PromptValidationError

logger = logging.getLogger(__name__)



class MasterConsultant:
    def __init__(self, name: str, system_instructions: str, assistant_instructions: str, openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.assistant_instructions = assistant_instructions
        self.llm_client = openai_client

    async def is_alive(self):
        try:
            await self.llm_client.list_models()
            return True
        except Exception:
            return False

    async def master_consult(self, prompt: PromptRequest, master_grader_report: MasterGradeReportResponse) -> MasterConsultantReportResponse:
        try:
            logger.info(f"[{self.name}] Starting assistant consultants...")
            consultant_categories = ["clarity", "specificity", "complexity", "completeness","consistency"]
            tasks = []
            for category in consultant_categories:
                instruction = self.assistant_instructions.get(category)
                if not instruction:
                    raise ValueError(f"Missing Instructions for: {category}")
                consultant = AssistantConsultant(
                    name=f"{category.capitalize()} Consultant",
                    system_instructions=instruction,
                    openai_client=self.llm_client
                )
                tasks.append(consultant.consult(prompt=prompt, grade_report=master_grader_report.grade_reports[category]))
            results = await asyncio.gather(*tasks)
            logger.info(f"[{self.name}] All assistant consultants finished.")

            reports = {category: result for category, result in zip(consultant_categories, results)}
            master_prompt = self._build_master_prompt(prompt=prompt, reports=reports, master_grader_report=master_grader_report)
            logger.info(f"[{self.name}] Sending master prompt to OpenAI...")

            suggestion_response: OverallSuggestionResponse = await self.llm_client.master_consult_prompt(
                prompt=master_prompt,
                system_instructions=self.system_instructions
            )
            logger.info(f"[{self.name}] Received master consultant suggestion.")

            return MasterConsultantReportResponse(
                consultant_reports=reports,
                overall_suggestion=suggestion_response.overall_suggestion
            )

        except PromptValidationError as ve:
            logger.warning(f"[{self.name}] Validation error: {ve}")
            raise ve

        except OpenAIServiceError as oe:
            logger.error(f"[{self.name}] OpenAI service error: {oe}")
            raise oe

        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error in master_consult: {e}")
            raise OpenAIServiceError(f"Unexpected error in MasterConsultant: {e}") from e

    def _build_master_prompt(self, prompt: PromptRequest, reports: Dict[str, ConsultantReportResponse], master_grader_report: MasterGradeReportResponse) -> PromptRequest:
        report_sections = "\n".join(
            f"""## {category.capitalize()} Consultant:
    - Suggestion: {report.suggestion}
    """
            for category, report in reports.items()
        )

        grading_sections = "\n".join(
            f"""## {category.capitalize()} Grader:
    - Score: {grade_report.score}
    - Reasoning: {grade_report.reasoning}
    """
            for category, grade_report in master_grader_report.grade_reports.items()
        )

        overall_score_section = f"""## Overall Grader Feedback:
    - Overall Score: {master_grader_report.overall_score}
    - Overall Feedback: {master_grader_report.overall_feedback}
    """

        refined_prompt = f"""
    # Original Prompt:
    {prompt.prompt}

    # Grading Reports:
    {grading_sections}

    # Consultant Suggestions:
    {report_sections}

    # Overall Grading Summary:
    {overall_score_section}
    """

        return PromptRequest(prompt=refined_prompt, tags=prompt.tags)
