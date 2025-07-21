from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class GradeReportResponse(BaseModel):
    score: int = Field(..., description="The score assigned to the prompt")
    reasoning: Optional[str] = Field(None, description="Reasoning behind the score")
    grader: Optional[str] = Field(None, description="Name of the grader")
class MasterGradeReportResponse(BaseModel):
    gradeReports: List[GradeReportResponse] = Field(..., description="List of grading reports for each category")
    overall_score: int = Field(..., description="Overall score based on all criteria")
    overall_feedback: Optional[str] = Field(None, description="Overall feedback on the prompt")
    