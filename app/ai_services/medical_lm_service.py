import logging
import json
from typing import List, Dict, Any, Generator, Optional
from google import genai
from google.genai import types
from flask import current_app

from .base import AIService
from .config import AI_SERVICE_CONFIG
from ..utils.mock_data import get_mock_medical_response, get_mock_structured_response

class MedicalLMService(AIService):
    """Implementation of AIService for Google's Medical LM models."""
    
    def __init__(self):
        """Initialize the Medical LM service."""
        config = AI_SERVICE_CONFIG.get("medical_lm", {})
        
        # Check if we're in development/local mode
        self.use_mock = current_app.config.get("FLASK_ENV") == "development" and current_app.config.get("USE_MOCK_AI", True)
        
        if not self.use_mock:
            self.client = genai.Client(
                vertexai=True,
                project=config.get("project"),
                location=config.get("location"),
            )
        else:
            logging.info("Using mock AI responses for Medical LM service")
            
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
        else:
            config_params["response_mime_type"] = "text/plain"

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
            # If using mock responses in local/development environment
            if self.use_mock:
                # Check if we have a schema (structured response requested)
                if response_schema:
                    return get_mock_structured_response(response_schema)
                    
                # Extract content from the messages to determine context
                message_content = "\n".join([msg.get("content", "") for msg in messages])
                
                # Determine if SOAP format is needed
                is_soap_request = "soap" in message_content.lower() or (system_instruction and "soap" in system_instruction.lower())
                
                # Get mock response based on the request type
                mock_response = get_mock_medical_response(
                    is_soap=is_soap_request
                )
                
                return mock_response
                
            # Real API call for production
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
            # If using mock responses in local/development environment
            if self.use_mock:
                # Get full mock response
                message_content = "\n".join([msg.get("content", "") for msg in messages])
                is_soap_request = "soap" in message_content.lower() or (system_instruction and "soap" in system_instruction.lower())
                mock_response = get_mock_medical_response(
                    is_soap=is_soap_request,
                    response_schema=response_schema
                )
                
                # Split into chunks to simulate streaming
                chunk_size = 20  # characters per chunk
                for i in range(0, len(mock_response), chunk_size):
                    yield mock_response[i:i+chunk_size]
                    import time
                    time.sleep(0.1)  # Simulate delay between chunks
                return
            
            # Real API streaming for production    
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
