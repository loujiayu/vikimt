from .base import AIService
from .gemini_service import GeminiAIService

# Factory function to get the appropriate AI service
def get_ai_service(service_type="gemini") -> AIService:
    """Get an AI service implementation by type."""
    if service_type == "gemini":
        return GeminiAIService()
    else:
        raise ValueError(f"Unknown AI service type: {service_type}")
