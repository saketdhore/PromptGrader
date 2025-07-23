# app/exceptions/errors.py

class AppBaseException(Exception):
    """Base class for all custom exceptions."""
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class OpenAIServiceError(AppBaseException):
    """Raised when OpenAI service fails or is unreachable."""
    def __init__(self, message="OpenAI service error"):
        super().__init__(message, code="OPENAI_SERVICE_ERROR", status_code=502)


class PromptValidationError(AppBaseException):
    """Raised when a user prompt is invalid (semantically)."""
    def __init__(self, message="Invalid prompt"):
        super().__init__(message, code="PROMPT_VALIDATION_ERROR", status_code=400)


class NotReadyError(AppBaseException):
    """Raised when a service component isn't ready yet."""
    def __init__(self, message="Service not ready"):
        super().__init__(message, code="SERVICE_NOT_READY", status_code=503)


class DependencyUnavailableError(AppBaseException):
    """Raised when a critical dependency (e.g., LLM) is unavailable."""
    def __init__(self, message="Dependency not available"):
        super().__init__(message, code="DEPENDENCY_UNAVAILABLE", status_code=503)
