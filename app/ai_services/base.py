from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator, Optional

class AIService(ABC):
    """Base abstract class for AI service implementations."""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, Any]], 
                          system_instruction: Optional[str] = None) -> str:
        """Generate a complete response from the AI model."""
        pass
    
    @abstractmethod
    def generate_stream(self, messages: List[Dict[str, Any]], 
                        system_instruction: Optional[str] = None) -> Generator[str, None, None]:
        """Stream the response from the AI model."""
        pass
