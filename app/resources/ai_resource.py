from flask_restful import Resource
from flask import request, jsonify
from flask_login import login_required, current_user
from app.decorators import doctor_required
from app.gcs_service import GCSService
from app.ai_services import get_ai_service
import logging

class AIResource(Resource):
    PATIENT_GCS_BUCKET_NAME = "patientstorage"
    DOCTOR_GCS_BUCKET_NAME = "doctorstorage"
    
    def __init__(self):
        self.patient_gcs_service = GCSService(self.PATIENT_GCS_BUCKET_NAME)
        self.doctor_gcs_service = GCSService(self.DOCTOR_GCS_BUCKET_NAME)
        self.ai_service = get_ai_service("medical_lm")  # Use medical LM for healthcare-specific content

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
    
    @login_required
    @doctor_required
    def post(self, patient_id=None):
        """
        Generate SOAP notes using AI based on a patient's chat history.
        
        Args:
            doctor_id: The ID of the doctor (optional, uses current doctor if not provided)
            patient_id: The ID of the patient whose chat history to use
        """
        try:
            # If no doctor_id is provided, use the current doctor's ID
            if doctor_id is None:
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
            prompt = f"Generate SOAP notes based on this patient chat history:\n\n{chat_history}"
            messages = [{"type": "user", "content": prompt}]
            
            # Generate SOAP notes with the AI service
            soap_notes = self.ai_service.generate_response(messages, system_instruction)
            
            # Save to blob storage
            blob_name = f"{doctor_id}/soap_notes/{patient_id}"
            self.doctor_gcs_service.upload_text(soap_notes, blob_name)
            
            return {
                "message": "SOAP notes generated and saved successfully", 
                "soap_notes": soap_notes,
                "patient_id": patient_id,
                "doctor_id": doctor_id
            }, 201
            
        except Exception as e:
            logging.error(f"Error generating SOAP notes: {str(e)}")
            return {"error": "Failed to generate SOAP notes"}, 500
