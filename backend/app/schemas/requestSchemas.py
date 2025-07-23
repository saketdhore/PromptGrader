from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="The prompt text to be graded or refined.")
    tags: Optional[List[str]] = Field(None, description="Optional tags for categorizing the prompt.")

class RefinePromptRequest(BaseModel):
    original_prompt: PromptRequest = Field(..., description="The prompt text that is to be changed by the user.")
    user_prompt: PromptRequest = Field(..., description="The instructions given by the user to refine the prompt")