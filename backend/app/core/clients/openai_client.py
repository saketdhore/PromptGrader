from openai import OpenAI, AsyncOpenAI
import logging
import os
from dotenv import load_dotenv
from pydantic import ValidationError
from app.schemas.response_schemas import (
    ConsultantReportResponse,
    GradeReportResponse,
    OverallFeedbackResponse,
    OverallSuggestionResponse,
    PromptResponse,
)
from app.schemas.request_schemas import PromptRequest
from app.exceptions.errors import OpenAIServiceError, PromptValidationError
import httpx

logger = logging.getLogger(__name__)
load_dotenv()


class OpenAIClient:
    def __init__(self, async_mode: bool = True):
        if os.getenv("ENV") == "test":
            raise RuntimeError("OpenAI calls are disabled in test mode")

        if os.getenv("GITHUB_ACTIONS") != "true":
            load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        try:
            logger.info("Initializing OpenAI client...")
            self.client = AsyncOpenAI(api_key=api_key) if async_mode else OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully.")
        except httpx.HTTPError as e:
            raise OpenAIServiceError(f"Failed to reach OpenAI: {e}") from e

    async def list_models(self):
        return await self.client.models.list()

    async def is_alive(self) -> bool:
        try:
            await self.list_models()
            return True
        except Exception:
            return False

    async def grade_prompt(self, grade_request: PromptRequest, system_instructions: str) -> GradeReportResponse:
        try:
            if not isinstance(grade_request.prompt, (str, list)):
                raise PromptValidationError("grade_request.prompt must be a string or a list of messages.")

            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=grade_request.prompt,
                instructions=system_instructions,
                text_format=GradeReportResponse,
                temperature=0,
            )
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise PromptValidationError(str(ve)) from ve
        except Exception as e:
            logger.error(f"Failed to create grading response: {e}")
            raise OpenAIServiceError(f"Grading failed: {e}") from e

    async def mastergrade_prompt(self, prompt: PromptRequest, system_instructions: str) -> OverallFeedbackResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=OverallFeedbackResponse,
                temperature=0,
            )
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise PromptValidationError(str(ve)) from ve
        except Exception as e:
            logger.error(f"Failed to create master grading response: {e}")
            raise OpenAIServiceError(f"Master grading failed: {e}") from e

    async def consult_prompt(self, prompt: PromptRequest, system_instructions: str) -> ConsultantReportResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=ConsultantReportResponse,
                temperature=0,
            )
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise PromptValidationError(str(ve)) from ve
        except Exception as e:
            logger.error(f"Failed to create consultant response: {e}")
            raise OpenAIServiceError(f"Consulting failed: {e}") from e

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
            raise PromptValidationError(str(ve)) from ve
        except Exception as e:
            logger.error(f"Failed to create master consultation response: {e}")
            raise OpenAIServiceError(f"Master consulting failed: {e}") from e

    async def engineer_prompt(self, prompt: PromptRequest, system_instructions: str) -> PromptResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=PromptResponse,
                temperature=0,
            )
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise PromptValidationError(str(ve)) from ve
        except Exception as e:
            logger.error(f"Failed to create engineer response: {e}")
            raise OpenAIServiceError(f"Engineering failed: {e}") from e

    async def refine_prompt(self, prompt: PromptRequest, system_instructions: str) -> PromptResponse:
        try:
            response = await self.client.responses.parse(
                model=os.getenv("OPENAI_MODEL"),
                input=prompt.prompt,
                instructions=system_instructions,
                text_format=PromptResponse,
                temperature=0,
            )
            logger.info(f"[OpenAIClient] Raw response from OpenAI: {response}")
            return response.output_parsed

        except ValidationError as ve:
            logger.error(f"Validation error parsing OpenAI response: {ve}")
            raise PromptValidationError(str(ve)) from ve
        except Exception as e:
            logger.error(f"Failed to create refiner response: {e}")
            raise OpenAIServiceError(f"Refining failed: {e}") from e