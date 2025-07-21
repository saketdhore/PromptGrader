from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class GradeReportResponse(BaseModel):
    score: int = Field(..., description="The score assigned to the prompt")
    feedback: Optional[str] = Field(None, description="Feedback on the prompt")
    grader: Optional[str] = Field(None, description="Name of the grader")
    