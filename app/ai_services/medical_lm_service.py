import logging
import json
from typing import List, Dict, Any, Generator, Optional
from google import genai
from google.genai import types
from app.config import Config

from .base import AIService
from .config import AI_SERVICE_CONFIG

class MedicalLMService(AIService):
    """Implementation of AIService for Google's Medical LM models."""
    
    def __init__(self):
        """Initialize the Medical LM service."""
        config = AI_SERVICE_CONFIG.get("medical_lm", {})

        if app.config.get("FLASK_ENV") == "development":
          config = AI_SERVICE_CONFIG.get("medical_lm", {})

        self.client = genai.Client(
            vertexai=True,
            project=config.get("project"),
            location=config.get("location"),
        )
        self.model_name = config.get("model_name")
        self.config = config
        
    def _convert_messages_to_contents(self, messages: List[Dict[str, Any]]) -> List[types.Content]:
        """Convert UI message format to Google AI content format."""
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
    
    def _create_generate_config(self, system_instruction: Optional[str] = None,
                               response_mime_type: Optional[str] = None,
                               response_schema: Optional[Dict[str, Any]] = None) -> types.GenerateContentConfig:
        """Create a configuration object for content generation."""
        safety_settings = [
            types.SafetySetting(category=setting["category"], threshold=setting["threshold"])
            for setting in self.config.get("safety_settings", [])
        ]
        
        # Base configuration parameters
        config_params = {
            "temperature": self.config.get("temperature", 0.2),  # Lower temperature for medical precision
            "top_p": self.config.get("top_p", 0.95),
            "max_output_tokens": self.config.get("max_output_tokens", 1024),
            "response_modalities": ["TEXT"],
            "safety_settings": safety_settings,
        }
        
        # Add system instruction if provided
        if system_instruction:
            config_params["system_instruction"] = system_instruction
        
        # Add response_mime_type if provided
        if response_mime_type:
            config_params["response_mime_type"] = response_mime_type
        
        # Add response_schema if provided
        if response_schema:
            config_params["response_schema"] = response_schema
        
        return types.GenerateContentConfig(**config_params)
    
    def generate_response(self, messages: List[Dict[str, Any]], 
                          system_instruction: Optional[str] = None,
                          response_mime_type: Optional[str] = None,
                          response_schema: Optional[Dict[str, Any]] = None) -> str:
        """Generate a complete response from the Medical LM model."""
        try:
            contents = self._convert_messages_to_contents(messages)
            generate_config = self._create_generate_config(
                system_instruction,
                response_mime_type, 
                response_schema
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=generate_config
            )
            
            return response.text
        except Exception as e:
            logging.error(f"Error generating response from Medical LM: {str(e)}")
            raise
    
    def generate_stream(self, messages: List[Dict[str, Any]], 
                        system_instruction: Optional[str] = None,
                        response_mime_type: Optional[str] = None,
                        response_schema: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """Stream the response from the Medical LM model."""
        try:
            contents = self._convert_messages_to_contents(messages)
            generate_config = self._create_generate_config(
                system_instruction,
                response_mime_type, 
                response_schema
            )
            
            stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=generate_config
            )
            
            for chunk in stream:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logging.error(f"Error streaming response from Medical LM: {str(e)}")
            raise
