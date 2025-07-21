from openai import OpenAI
from openai import AsyncOpenAI
import logging
import os
from pydantic import ValidationError
from app.schemas.responseSchemas import ConsultantReportResponse, GradeReportResponse, OverallFeedbackResponse, OverallSuggestionResponse, EngineerReportResponse
from app.schemas.requestSchemas import PromptRequest

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, async_mode: bool = True):
        try:
            logger.info("Initializing OpenAI client...")
            self.client = AsyncOpenAI() if async_mode else OpenAI()
            logger.info("OpenAI client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise  # Stops execution, surfaces the error
    async def grade_prompt(self, grade_request: PromptRequest, system_instructions: str) -> GradeReportResponse:
        try:
            # Validate the prompt is a string or list of dicts
            if not isinstance(grade_request.prompt, (str, list)):
                raise ValueError("grade_request.prompt must be a string or a list of messages.")
            
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=grade_request.prompt,
                instructions=system_instructions,
                text_format=GradeReportResponse,
                temperature=0,
            )

            # Pydantic validation happens automatically via text_format (GradeReportResponse)
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create grading response: {e}")
            raise e
    async def mastergrade_prompt(self, prompt: PromptRequest, system_instructions: str) -> OverallFeedbackResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=OverallFeedbackResponse,
                temperature=0,
            )

            # Pydantic validation happens automatically via text_format (OverallFeedbackResponse)
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create master grading response: {e}")
            raise e
    
    async def consult_prompt(self, prompt: PromptRequest, system_instructions: str) -> ConsultantReportResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=ConsultantReportResponse,
                temperature=0,
            )

            # Pydantic validation happens automatically via text_format (ConsultantReportResponse)
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create consultant response: {e}")
            raise e
    async def master_consult_prompt(self, prompt: PromptRequest, system_instructions: str) -> OverallSuggestionResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=OverallSuggestionResponse,
                temperature=0,
            )

            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create master consultation response: {e}")
            raise e
    async def engineer_prompt(self, prompt: PromptRequest, system_instructions: str) -> PromptRequest:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=PromptRequest,
                temperature=0,
            )
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"Failed to create engineer response: {e}")
            raise e
