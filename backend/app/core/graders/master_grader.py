import logging
import asyncio
from typing import Dict
from app.core.graders.assistant_grader import AssistantGrader
from app.schemas.request_schemas import PromptRequest
from app.schemas.response_schemas import (
    GradeReportResponse,
    MasterGradeReportResponse,
    OverallFeedbackResponse
)
from app.core.clients.openai_client import OpenAIClient
from app.exceptions.errors import OpenAIServiceError, PromptValidationError
logger = logging.getLogger(__name__)
class MasterGrader:
    def __init__(self, name: str, system_instructions: str, assistant_instructions: Dict[str, str], openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.assistant_instructions = assistant_instructions
        self.llm_client = openai_client        
    async def is_alive(self) -> bool:
        try:
            await self.llm_client.list_models()
            return True
        except Exception:
            return False

    async def master_grade(self, prompt: PromptRequest) -> MasterGradeReportResponse:
        try:
            logger.info(f"[{self.name}] Starting assistant graders for prompt.")
            grader_categories = ["clarity", "specificity", "complexity", "completeness","consistency"]
            tasks = []

            for category in grader_categories:
                instruction = self.assistant_instructions.get(category)
                if not instruction:
                    raise ValueError(f"Missing instruction for {category}")
                
                grader = AssistantGrader(
                    name=f"{category.capitalize()} Grader",
                    system_instructions=instruction,
                    openai_client=self.llm_client
                )
                tasks.append(grader.grade(prompt))

            results = await asyncio.gather(*tasks)
            reports = {category: result for category, result in zip(grader_categories, results)}

            overall_score = sum(report.score for report in reports.values()) // len(reports)

            master_prompt = self._build_master_prompt(prompt=prompt, reports=reports, overall_score=overall_score)

            logger.info(f"[{self.name}] Requesting overall feedback from OpenAI.")
            feedback_response: OverallFeedbackResponse = await self.llm_client.mastergrade_prompt(
                prompt=master_prompt,
                system_instructions=self.system_instructions
            )

            logger.info(f"[{self.name}] Master grading completed successfully.")
            return MasterGradeReportResponse(
                grade_reports=reports,
                overall_score=overall_score,
                overall_feedback=feedback_response.overall_feedback
            )

        except PromptValidationError as ve:
            logger.warning(f"[{self.name}] Prompt validation error: {ve}")
            raise ve

        except OpenAIServiceError as oe:
            logger.error(f"[{self.name}] OpenAI service error: {oe}")
            raise oe

        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error during master grading: {e}")
            raise OpenAIServiceError(f"Unexpected error in MasterGrader: {e}") from e

    def _build_master_prompt(self, prompt: PromptRequest, reports: Dict[str, GradeReportResponse], overall_score: int) -> PromptRequest:
        report_sections = "\n".join(
            f"""## {category.capitalize()}:
    Score: {report.score}
    Reasoning: {report.reasoning}
    """ for category, report in reports.items()
        )
        refined_prompt = f"""
    # Original Prompt:
    {prompt.prompt}

    # Grading Reports:
    {report_sections}

    # Overall Score:
    {overall_score}/100
    """
        return PromptRequest(prompt=refined_prompt, tags=prompt.tags)