from pydantic import BaseModel, Field, field_validator
from typing import List

MAX_WORDS = 1000
MAX_TAGS = 5

class PromptRequest(BaseModel):
    prompt: str = Field(..., description=f"Prompt with up to {MAX_WORDS} words")
    tags: List[str] = Field(default=[])

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v):
        if isinstance(v, str):
            if not v.strip():
                raise ValueError("Prompt must not be empty or whitespace.")
            word_count = len(v.split())
            if word_count > MAX_WORDS:
                raise ValueError(f"Prompt exceeds the {MAX_WORDS}-word limit (got {word_count} words).")
        elif isinstance(v, list):
            if not v:
                raise ValueError("Prompt list must not be empty.")
        else:
            raise ValueError("Prompt must be a string or a list.")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags):
        if len(tags) > MAX_TAGS:
            raise ValueError(f"You can only provide up to {MAX_TAGS} tags.")
        return tags

class RefinePromptRequest(BaseModel):
    original_prompt: PromptRequest = Field(..., description="The prompt text that is to be changed by the user.")
    user_prompt: PromptRequest = Field(..., description="The instructions given by the user to refine the prompt")
