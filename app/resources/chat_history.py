from flask_restful import Resource
from flask import jsonify, request
from google.cloud import storage
from flask_login import login_user, logout_user, login_required
from app.gcs_service import GCSService
from app.ai_services import get_ai_service
from app.models.patient import Patient
from app import db
import json
import logging

class UserType:
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    VALID_TYPES = {PATIENT, DOCTOR}

class ChatHistoryResource(Resource):
    PATIENT_GCS_BUCKET_NAME = "patientstorage"
    DOCTOR_GCS_BUCKET_NAME = "doctorstorage"
    
    def __init__(self):
        self.patient_gcs_service = GCSService(self.PATIENT_GCS_BUCKET_NAME)
        self.doctor_gcs_service = GCSService(self.DOCTOR_GCS_BUCKET_NAME)
        self.ai_service = get_ai_service("gemini")
    
    @login_required
    def get(self, user_id):
        """
        Retrieve chat history for a specific user
        """
        user_type = request.args.get('user_type')
        
        if user_type not in UserType.VALID_TYPES:
            return {'message': 'Invalid user type.'}, 400
        
        chat_history = self.get_history_from_gcs(user_type, user_id)
        if not chat_history:
            return {'message': 'No chat history found for this user.'}, 404
        
        return {'content': chat_history}, 200
    
    @login_required
    def post(self, user_id):
        """
        Save or update chat history for a specific user
        """
        user_type = request.args.get('user_type')
        
        if user_type not in UserType.VALID_TYPES:
            return {'message': 'Invalid user type.'}, 400
        
        history_data = request.get_json()
        if not history_data or 'content' not in history_data:
            return {'message': 'No valid chat history data provided.'}, 400

        history_data_content = history_data['content']
        
        # Save history to GCS
        self.save_history_to_gcs(user_type, user_id, history_data_content)
        
        # Process with AI service if this is patient data
        if user_type == UserType.PATIENT:
            try:
                self.process_with_ai_service(user_id, history_data_content)
            except Exception as e:
                logging.error(f"Error processing chat history with AI service: {str(e)}")
                # Continue execution even if AI processing fails
        
        return {'message': 'Chat history saved successfully.'}, 201
    
    def get_history_from_gcs(self, user_type, user_id):
        blob_path = f"{user_id}/chat_history"
        gcs_service = self.doctor_gcs_service if user_type == UserType.DOCTOR else self.patient_gcs_service
        data = gcs_service.download_text(blob_path)
        return data
    
    def save_history_to_gcs(self, user_type, user_id, history_data):
        blob_path = f"{user_id}/chat_history"
        gcs_service = self.doctor_gcs_service if user_type == UserType.DOCTOR else self.patient_gcs_service
        gcs_service.upload_text(history_data, blob_path)
    
    def process_with_ai_service(self, patient_id, chat_content):
        """
        Process chat history with AI service and update patient metadata.
        
        Args:
            patient_id (str): The ID of the patient
            chat_content (str): The chat history content
        """
        # Define the schema as specified
        response_schema = {
            "type": "object",
            "properties": {
                "Risk": {
                    "type": "string",
                    "enum": ["High", "Medium", "Low"],
                    "description": "The level of risk associated with the condition."
                },
                "Condition": {
                    "type": "string",
                    "description": "The medical condition diagnosed."
                },
                "Age": {
                    "type": "integer",
                    "format": "int32",
                    "description": "The age of the patient."
                },
                "LastVisit": {
                    "type": "string",
                    "format": "date",
                    "description": "The date of the patient's last medical visit in YYYY-MM-DD format."
                }
            },
            "required": ["Risk", "Condition"]
        }
        
        # Create system instruction for Gemini
        system_instruction = (
            "You are a medical analysis AI. Analyze the patient conversation with chatbot and extract key information. "
            "Include the patient's risk level (High/Medium/Low), medical condition, age (if mentioned), "
            "and last visit date in YYYY-MM-DD format (if mentioned)."
        )
        
        # Format message for the AI service
        prompt = (
            f"Analyze this patient conversation and extract key medical information:\n\n"
            f"{chat_content}"
        )
        
        messages = [{"type": "user", "content": prompt}]
        
        # Call the AI service with the response schema
        ai_response = self.ai_service.generate_response(
            messages, 
            system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema
        )
        
        # Extract JSON from response
        try:
            # Try to parse the entire response as JSON
            parsed_response = json.loads(ai_response)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the text using regex
            import re
            json_match = re.search(r'({[\s\S]*})', ai_response)
            if json_match:
                try:
                    parsed_response = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    logging.error("Failed to extract valid JSON from AI response")
                    return
            else:
                logging.error("No JSON found in AI response")
                return
        
        # Update patient metadata with AI analysis
        patient = Patient.query.get(patient_id)
        if patient:
            # Initialize metadata if None
            current_metadata = patient.patient_metadata or {}
            
            # Merge with existing metadata
            if isinstance(current_metadata, dict):
                current_metadata.update(parsed_response)
            else:
                current_metadata = parsed_response
            
            # Update patient record
            patient.patient_metadata = current_metadata
            db.session.commit()
            logging.info(f"Updated metadata for patient {patient_id}")
