from flask_restful import Resource
from flask import jsonify, request
from google.cloud import storage
from flask_login import login_user, logout_user, login_required
from app.gcs_service import GCSService

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
        
        self.save_history_to_gcs(user_type, user_id, history_data_content)
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
