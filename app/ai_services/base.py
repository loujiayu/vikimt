from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator, Optional

class AIService(ABC):
    """Base abstract class for AI service implementations."""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, Any]], 
                          system_instruction: Optional[str] = None,
                          response_mime_type: Optional[str] = None,
                          response_schema: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a complete response from the AI model.
        
        Args:
            messages: List of message dictionaries with 'type' and 'content'
            system_instruction: Optional system instruction for the AI
            response_mime_type: Optional MIME type for the response format (e.g., "application/json")
            response_schema: Optional JSON schema for structured output
            
        Returns:
            str: The generated response
        """
        pass
    
    @abstractmethod
    def generate_stream(self, messages: List[Dict[str, Any]], 
                        system_instruction: Optional[str] = None,
                        response_mime_type: Optional[str] = None,
                        response_schema: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """
        Stream the response from the AI model.
        
        Args:
            messages: List of message dictionaries with 'type' and 'content'
            system_instruction: Optional system instruction for the AI
            response_mime_type: Optional MIME type for the response format (e.g., "application/json")
            response_schema: Optional JSON schema for structured output
            
        Returns:
            Generator yielding response chunks
        """
        pass
