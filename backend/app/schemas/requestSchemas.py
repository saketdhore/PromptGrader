from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="The prompt text to be graded or refined.")
    tags: Optional[List[str]] = Field(None, description="Optional tags for categorizing the prompt.")
    