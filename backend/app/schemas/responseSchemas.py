from pydantic import BaseModel, Field
from app.schemas.requestSchemas import PromptRequest
from typing import Optional, Dict



class GradeReportResponse(BaseModel):
    score: int = Field(..., description="The score assigned to the prompt")
    reasoning: str = Field(..., description="Reasoning behind the score")
    grader: str = Field(..., description="Name of the grader")


class MasterGradeReportResponse(BaseModel):
    grade_reports: Dict[str, GradeReportResponse] = Field(..., description="Map of grading reports for each category")
    overall_score: int = Field(..., description="Overall score based on all criteria")
    overall_feedback: str = Field(..., description="Overall feedback on the prompt")


class OverallFeedbackResponse(BaseModel):
    overall_score: int = Field(..., description="Overall score for the prompt")
    overall_feedback: str = Field(..., description="Overall feedback for the prompt")


class OverallSuggestionResponse(BaseModel):
    overall_suggestion: str = Field(..., description="Overall suggestion for improving the prompt")

class ConsultantReportResponse(BaseModel):
    suggestion: str = Field(..., description="Consultant's suggestion for improving the prompt")
    consultant: str = Field(..., description="Name of the consultant")


class MasterConsultantReportResponse(BaseModel):
    consultant_reports: Dict[str, ConsultantReportResponse] = Field(..., description="Map of consultant reports for each category")
    overall_suggestion: str = Field(..., description="Overall suggestion for improving the prompt")

class EngineerReportResponse(BaseModel):
    original_prompt: PromptRequest = Field(..., description="The original prompt provided by the user")
    refined_prompt: PromptRequest = Field(..., description="The refined prompt after engineering")