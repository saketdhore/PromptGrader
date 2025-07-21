from openai import OpenAI
import logging
import os
from pydantic import ValidationError
from app.schemas.responseSchemas import GradeReportResponse, OverallFeedbackResponse
from app.schemas.requestSchemas import PromptRequest

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        try:
            logger.info("Initializing OpenAI client...")
            self.client = OpenAI()
            logger.info("OpenAI client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise  # Stops execution, surfaces the error
    def grade_prompt(self, grade_request: PromptRequest, system_instructions: str) -> GradeReportResponse:
        try:
            # Validate the prompt is a string or list of dicts
            if not isinstance(grade_request.prompt, (str, list)):
                raise ValueError("grade_request.prompt must be a string or a list of messages.")
            
            response = self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=grade_request.prompt,
                instructions=system_instructions,
                text_format=GradeReportResponse,
                temperature=0,
            )

            # Pydantic validation happens automatically via text_format (GradeReportResponse)
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create grading response: {e}")
            raise e
    def mastergrade_prompt(self, prompt: PromptRequest, system_instructions: str) -> OverallFeedbackResponse:
        try:
            response = self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=OverallFeedbackResponse,
                temperature=0,
            )

            # Pydantic validation happens automatically via text_format (OverallFeedbackResponse)
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create master grading response: {e}")
            raise e

            