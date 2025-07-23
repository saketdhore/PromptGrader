import logging
import asyncio
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import EngineerReportResponse, MasterConsultantReportResponse, MasterGradeReportResponse
from app.exceptions.errors import OpenAIServiceError, PromptValidationError

logger = logging.getLogger(__name__)

class Engineer:
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

    async def engineer(self, prompt: PromptRequest, master_consultant_report: MasterConsultantReportResponse, master_grade_report: MasterGradeReportResponse) -> EngineerReportResponse:
        try:
            logger.info(f"[{self.name}] Engineering prompt: {prompt.prompt[0:50]}...")
            engineer_prompt = self._build_master_prompt(
                prompt=prompt,
                master_consultant_report=master_consultant_report,
                master_grade_report=master_grade_report
            )

            refined_prompt = await self.llm_client.engineer_prompt(
                prompt=engineer_prompt,
                system_instructions=self.system_instructions
            )

            logger.info(f"[{self.name}] Engineering completed successfully.")
            return EngineerReportResponse(
                original_prompt=prompt,
                refined_prompt=refined_prompt
            )

        except PromptValidationError as ve:
            logger.warning(f"[{self.name}] Validation error during engineering: {ve}")
            raise ve

        except OpenAIServiceError as oe:
            logger.error(f"[{self.name}] OpenAI service error during engineering: {oe}")
            raise oe

        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error during engineering: {e}")
            raise OpenAIServiceError(f"Unexpected error in Engineer: {e}") from e

    def _build_master_prompt(self, prompt: PromptRequest, master_consultant_report: MasterConsultantReportResponse, master_grade_report: MasterGradeReportResponse) -> PromptRequest:
        grading_sections = "\n".join(
            f"""## {category.capitalize()} Grader Feedback:
    - Score: {grade.score}
    - Reasoning: {grade.reasoning}"""
            for category, grade in master_grade_report.grade_reports.items()
        )

        overall_grading_summary = f"""## Overall Grader Feedback:
    - Overall Score: {master_grade_report.overall_score}
    - Feedback: {master_grade_report.overall_feedback}
    """

        consultant_sections = "\n".join(
            f"""## {category.capitalize()} Consultant Suggestion:
    - {report.suggestion}"""
            for category, report in master_consultant_report.consultant_reports.items()
        )

        overall_consultant_suggestion = f"""## Overall Consultant Suggestion:
    - {master_consultant_report.overall_suggestion}
    """

        engineer_prompt_content = f"""
    # Original Prompt:
    {prompt.prompt}

    # Grading Reports:
    {grading_sections}

    # Overall Grading Summary:
    {overall_grading_summary}

    # Consultant Suggestions:
    {consultant_sections}

    # Overall Consultant Suggestion:
    {overall_consultant_suggestion}
    """

        return PromptRequest(prompt=engineer_prompt_content.strip(), tags=prompt.tags)
