from typing import Dict
from app.core.clients.openai_client import OpenAIClient
from app.core.consultants.assistant_consultant import AssistantConsultant   
from app.schemas.requestSchemas import PromptRequest
import asyncio
import logging
from app.schemas.responseSchemas import (
    MasterConsultantReportResponse,
    ConsultantReportResponse,
    MasterGradeReportResponse,
    OverallSuggestionResponse
)
from app.core.instructions.consultant_instructions import (
    CLARITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    SPECIFICITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    COMPLEXITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    COMPLETENESS_CONSULTANT_SYSTEM_INSTRUCTIONS,
    CONSISTENCY_CONSULTANT_SYSTEM_INSTRUCTIONS,
)

logger = logging.getLogger(__name__)

CATEGORIES = [
    ("clarity", CLARITY_CONSULTANT_SYSTEM_INSTRUCTIONS),
    ("specificity", SPECIFICITY_CONSULTANT_SYSTEM_INSTRUCTIONS),
    ("complexity", COMPLEXITY_CONSULTANT_SYSTEM_INSTRUCTIONS),
    ("completeness", COMPLETENESS_CONSULTANT_SYSTEM_INSTRUCTIONS),
    ("consistency", CONSISTENCY_CONSULTANT_SYSTEM_INSTRUCTIONS),
]
class MasterConsultant:
    def __init__(self, name: str, system_instructions: str, openai_client: OpenAIClient):
        self.name = name
        self.system_instructions = system_instructions
        self.llm_client = openai_client
    async def master_consult(self, prompt: PromptRequest, master_grader_report: MasterGradeReportResponse) -> MasterConsultantReportResponse:
        try:
            logger.info(f"[{self.name}] Starting assistant consultants...")
            tasks = [
                AssistantConsultant(
                    name=f"{category.capitalize()} Consultant",
                    system_instructions=instructions,
                    openai_client=self.llm_client
                ).consult(
                    prompt=prompt,
                    grade_report=master_grader_report.grade_reports[category]
                )
                for category, instructions in CATEGORIES
            ]
            
            results = await asyncio.gather(*tasks)
            logger.info(f"[{self.name}] All assistant consultants finished.")

            reports = {category: result for (category, _), result in zip(CATEGORIES, results)}
            logger.info(f"[{self.name}] Building master prompt...")
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
        except Exception as e:
            logger.error(f"[{self.name}] Error during master consultation: {e}")
            raise e
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
