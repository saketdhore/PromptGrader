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
from app.core.instructions.grader_instructions import (
    CLARITY_GRADER_SYSTEM_INSTRUCTIONS,
    SPECIFICITY_GRADER_SYSTEM_INSTRUCTIONS,
    COMPLEXITY_GRADER_SYSTEM_INSTRUCTIONS,
    COMPLETENESS_GRADER_SYSTEM_INSTRUCTIONS,
    CONSISTENCY_GRADER_SYSTEM_INSTRUCTIONS,
)
from app.core.clients.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

CATEGORIES = [
    ("clarity", CLARITY_GRADER_SYSTEM_INSTRUCTIONS),
    ("specificity", SPECIFICITY_GRADER_SYSTEM_INSTRUCTIONS),
    ("complexity", COMPLEXITY_GRADER_SYSTEM_INSTRUCTIONS),
    ("completeness", COMPLETENESS_GRADER_SYSTEM_INSTRUCTIONS),
    ("consistency", CONSISTENCY_GRADER_SYSTEM_INSTRUCTIONS),
]

class MasterGrader:
    def __init__(self, name: str, system_instructions: str, openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client

    async def master_grade(self, prompt: PromptRequest) -> MasterGradeReportResponse:
        try:
            tasks = [
                AssistantGrader(
                    name=f"{category.capitalize()} Grader",
                    system_instructions=instructions,
                    openai_client=self.llm_client
                ).grade(prompt)
                for category, instructions in CATEGORIES
            ]

            results = await asyncio.gather(*tasks)
            reports = {category: result for (category, _), result in zip(CATEGORIES, results)}

            overall_score = sum(report.score for report in reports.values()) // len(reports)

            master_prompt = self._build_master_prompt(prompt=prompt, reports=reports, overall_score=overall_score)


            feedback_response: OverallFeedbackResponse = await self.llm_client.mastergrade_prompt(
                prompt=master_prompt,
                system_instructions=self.system_instructions
            )

            return MasterGradeReportResponse(
                grade_reports=reports,
                overall_score=overall_score,
                overall_feedback=feedback_response.overall_feedback
            )


        except Exception as e:
            logger.error(f"Error grading prompt: {e}")
            raise e

    def _build_master_prompt(self, prompt: PromptRequest, reports: Dict[str, GradeReportResponse], overall_score: int) -> PromptRequest:
        report_sections = "\n".join(
            f"""## {category.capitalize()}:
    Score: {report.score}
    Reasoning: {report.reasoning}
    """ for category, report in reports.items()
        )
        refined_prompt =f"""
    # Original Prompt:
    {prompt.prompt}

    # Grading Reports:
    {report_sections}

    # Overall Score:
    {overall_score}/100
    """
        return PromptRequest(prompt=refined_prompt, tags=prompt.tags)



