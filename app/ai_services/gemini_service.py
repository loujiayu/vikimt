import logging
from typing import List, Dict, Any, Generator, Optional
from google import genai
from google.genai import types

from .base import AIService
from .config import AI_SERVICE_CONFIG

class GeminiAIService(AIService):
    """Implementation of AIService for Google's Gemini models."""
    
    def __init__(self):
        """Initialize the Gemini AI service."""
        config = AI_SERVICE_CONFIG.get("gemini", {})
        self.client = genai.Client(
            vertexai=True,
            project=config.get("project"),
            location=config.get("location"),
        )
        self.model_name = config.get("model_name")
        self.config = config
        
    def _convert_messages_to_contents(self, messages: List[Dict[str, Any]]) -> List[types.Content]:
        """Convert UI message format to Gemini content format."""
        role_mapping = {
            "assistant": "model",
            "user": "user"
        }
        
        contents = [
            types.Content(
                role=role_mapping[item["type"]],
                parts=[types.Part.from_text(text=item["content"])]
            )
            for item in messages
        ]
        
        return contents
    
    def _create_generate_config(self, system_instruction: Optional[str] = None) -> types.GenerateContentConfig:
        """Create a configuration object for content generation."""
        safety_settings = [
            types.SafetySetting(category=setting["category"], threshold=setting["threshold"])
            for setting in self.config.get("safety_settings", [])
        ]
        
        return types.GenerateContentConfig(
            temperature=self.config.get("temperature", 1.0),
            top_p=self.config.get("top_p", 0.95),
            max_output_tokens=self.config.get("max_output_tokens", 1024),
            response_modalities=["TEXT"],
            safety_settings=safety_settings,
            system_instruction=system_instruction
        )
    
    def generate_response(self, messages: List[Dict[str, Any]], 
                          system_instruction: Optional[str] = None) -> str:
        """Generate a complete response from the Gemini model."""
        try:
            contents = self._convert_messages_to_contents(messages)
            generate_config = self._create_generate_config(system_instruction)
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=generate_config
            )
            
            return response.text
        except Exception as e:
            logging.error(f"Error generating response from Gemini: {str(e)}")
            raise
    
    def generate_stream(self, messages: List[Dict[str, Any]], 
                        system_instruction: Optional[str] = None) -> Generator[str, None, None]:
        """Stream the response from the Gemini model."""
        try:
            contents = self._convert_messages_to_contents(messages)
            generate_config = self._create_generate_config(system_instruction)
            
            stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=generate_config
            )
            
            for chunk in stream:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logging.error(f"Error streaming response from Gemini: {str(e)}")
            raise
