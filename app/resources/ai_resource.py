from flask_restful import Resource
from flask import request, jsonify
from flask_login import login_required, current_user
from app.decorators import doctor_required
from app.gcs_service import GCSService
from app.ai_services import get_ai_service
import logging
import json

class AIResource(Resource):
    PATIENT_GCS_BUCKET_NAME = "patientstorage"
    DOCTOR_GCS_BUCKET_NAME = "doctorstorage"
    
    def __init__(self, method_type='soap'):
        self.patient_gcs_service = GCSService(self.PATIENT_GCS_BUCKET_NAME)
        self.doctor_gcs_service = GCSService(self.DOCTOR_GCS_BUCKET_NAME)
        self.ai_service = get_ai_service("medical_lm")
        self.method_type = method_type  # Store the method type ('soap' or 'dvx')
    
    def get_soap_prompt(self, doctor_id):
        """
        Retrieve SOAP prompt from blob storage for a specific doctor.
        
        Args:
            doctor_id: The ID of the doctor
            
        Returns:
            The SOAP prompt content or None if not found
        """
        try:
            # Format the blob name as specified
            blob_name = f"{doctor_id}/soap"
            
            # Get content from doctor's blob storage
            soap_content = self.doctor_gcs_service.download_text(blob_name)
            
            return soap_content
        except Exception as e:
            logging.error(f"Error getting SOAP prompt from blob storage: {str(e)}")
            return None
    
    def get_chat_history(self, patient_id):
        """
        Retrieve chat history from blob storage for a specific patient.
        
        Args:
            patient_id: The ID of the patient
            
        Returns:
            The chat history content or None if not found
        """
        try:
            # Format the blob name as specified
            blob_name = f"{patient_id}/chat_history"
            
            # Get content from patient's blob storage
            chat_history = self.patient_gcs_service.download_text(blob_name)
            
            return chat_history
        except Exception as e:
            logging.error(f"Error getting chat history from blob storage: {str(e)}")
            return None

    def get_dvx_prompt(self, doctor_id):
        """
        Retrieve DVX prompt template from blob storage for a specific doctor.
        
        Args:
            doctor_id: The ID of the doctor
            
        Returns:
            The DVX prompt content or None if not found
        """
        try:
            # Format the blob name as specified
            blob_name = f"{doctor_id}/dvx"
            
            # Get content from doctor's blob storage
            dvx_content = self.doctor_gcs_service.download_text(blob_name)
            
            return dvx_content
        except Exception as e:
            logging.error(f"Error getting DVX prompt from blob storage: {str(e)}")
            return None
    
    @login_required
    @doctor_required
    def post(self, patient_id=None):
        """
        Route handler that delegates to the appropriate method based on endpoint type.
        """
        # Delegate to the appropriate method based on the method_type
        if self.method_type == 'soap':
            return self.generate_soap_notes(patient_id)
        elif self.method_type == 'dvx':
            return self.generate_differential_diagnosis(patient_id)
        else:
            return {"error": f"Unknown method type: {self.method_type}"}, 400
    
    def generate_soap_notes(self, patient_id=None):
        """Generate SOAP notes using AI based on a patient's chat history."""
        try:
            # If no doctor_id is provided, use the current doctor's ID
            if hasattr(current_user, 'doctor_id'):
                doctor_id = current_user.doctor_id
            else:
                return {"error": "No doctor ID available"}, 400
            
            # Ensure patient_id is provided
            if patient_id is None:
                return {"error": "Patient ID is required"}, 400
                
            # Get chat history from blob storage
            chat_history = self.get_chat_history(patient_id)
            if not chat_history:
                return {"error": f"No chat history found for patient {patient_id}"}, 404
                
            # Get SOAP prompt template from doctor's storage to use as system instruction
            system_instruction = self.get_soap_prompt(doctor_id)
            if not system_instruction:
                # Use default system instruction if no custom prompt exists
                system_instruction = (
                    "You are a medical assistant helping to generate SOAP notes from patient chat history. "
                    "SOAP stands for Subjective, Objective, Assessment, and Plan. "
                    "Provide a structured, professional medical SOAP note format."
                )
            
            # Create message with chat history
            prompt = f"{chat_history}"
            messages = [{"type": "user", "content": prompt}]
            
            # Log prompt and system instruction for debugging
            logging.info(f"System instruction for patient {patient_id}: {system_instruction}")
            logging.info(f"Prompt for patient {patient_id}: {prompt}")

            # Define structured response schema for SOAP notes
            response_schema = {
                "type": "OBJECT",
                "properties": {
                    "subjective": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "objective": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "assessment": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "plan": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                },
                "required": ["subjective", "objective", "assessment", "plan"]
            }

            # Generate SOAP notes with the AI service
            soap_notes = self.ai_service.generate_response(
                messages,
                system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema
            )
            
            return {
                "content": json.loads(soap_notes),
            }, 201
            
        except Exception as e:
            logging.error(f"Error generating SOAP notes: {str(e)}")
            return {"error": "Failed to generate SOAP notes"}, 500

    def generate_differential_diagnosis(self, patient_id=None):
        """Generate differential diagnosis using AI based on a patient's chat history."""
        try:
            # If no doctor_id is provided, use the current doctor's ID
            if hasattr(current_user, 'doctor_id'):
                doctor_id = current_user.doctor_id
            else:
                return {"error": "No doctor ID available"}, 400
            
            # Ensure patient_id is provided
            if patient_id is None:
                return {"error": "Patient ID is required"}, 400
                
            # Get chat history from blob storage
            chat_history = self.get_chat_history(patient_id)
            if not chat_history:
                return {"error": f"No chat history found for patient {patient_id}"}, 404
                
            # Get DVX prompt template from doctor's storage to use as system instruction
            system_instruction = self.get_dvx_prompt(doctor_id)
            if not system_instruction:
                # Use default system instruction if no custom prompt exists
                system_instruction = (
                    "You are a differential diagnosis assistant helping to analyze patient symptoms. "
                    "Based on the conversation history, generate a list of possible diagnoses with "
                    "risk levels, confidence percentages, and recommended next steps for each condition."
                )
            
            # Create message with chat history
            prompt = f"{chat_history}"
            messages = [{"type": "user", "content": prompt}]
            
            # Define structured response schema for differential diagnosis
            response_schema = {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "required": [
                        "condition",
                        "risk",
                        "confidence",
                        "steps"
                    ],
                    "properties": {
                        "condition": {
                            "type": "STRING"
                        },
                        "risk": {
                            "type": "STRING",
                            "enum": [
                                "Low",
                                "Moderate",
                                "Critical"
                            ]
                        },
                        "confidence": {
                            "type": "INTEGER",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "steps": {
                            "type": "STRING"
                        }
                    }
                }
            }
            
            # Log prompt and system instruction for debugging
            logging.info(f"DVX System instruction for patient {patient_id}: {system_instruction}")
            logging.info(f"DVX Prompt for patient {patient_id}: {prompt}")
            
            # Use the existing medical_lm_service for differential diagnosis
            differential_diagnosis = self.ai_service.generate_response(
                messages, 
                system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema
            )
            
            return {
                "content": json.loads(differential_diagnosis),
            }, 201
            
        except Exception as e:
            logging.error(f"Error generating differential diagnosis: {str(e)}")
            return {"error": "Failed to generate differential diagnosis"}, 500
