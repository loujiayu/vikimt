from flask_restful import Resource
from flask import jsonify, request
from google.cloud import storage
from flask_login import login_user, logout_user, login_required
from app.gcs_service import GCSService

class UserType:
	PATIENT = 'patient'
	DOCTOR = 'doctor'
	VALID_TYPES = {PATIENT, DOCTOR}

class PromptResource(Resource):
	PATIENT_GCS_BUCKET_NAME = "patientstorage"
	DOCTOR_GCS_BUCKET_NAME = "doctorstorage"
	
	def __init__(self):
		self.patient_gcs_service = GCSService(self.PATIENT_GCS_BUCKET_NAME)
		self.doctor_gcs_service = GCSService(self.DOCTOR_GCS_BUCKET_NAME)
		
	@login_required
	def get(self, user_id):
		user_type = request.args.get('user_type')
		prompt_blob = request.args.get('prompt_blob')
		
		if user_type not in UserType.VALID_TYPES:
			return {'message': 'Invalid user type.'}, 400
		
		if not prompt_blob:
			return {'message': 'Prompt blob is required.'}, 400
		
		prompt = self.get_prompt_from_gcs(user_type, user_id, prompt_blob)
		if not prompt:
			return {'message': 'No prompt found for this ID.'}, 404
		
		return jsonify(prompt)
	
	@login_required
	def post(self, user_id):
		user_type = request.args.get('user_type')
		prompt_blob = request.args.get('prompt_blob')
		
		if user_type not in UserType.VALID_TYPES:
			return {'message': 'Invalid user type.'}, 400
		
		if not prompt_blob:
			return {'message': 'Prompt blob is required.'}, 400
		
		# Assuming the prompt data is sent in the request body as JSON
		prompt_data = request.get_json()
		if not prompt_data:
			return {'message': 'No data provided.'}, 400
		
		self.save_prompt_to_gcs(user_type, user_id, prompt_blob, prompt_data)
		return {'message': 'Prompt saved successfully.'}, 201

	def get_prompt_from_gcs(self, user_type, user_id, prompt_blob):
		blob_name = f"{user_id}/{prompt_blob}"
		gcs_service = self.doctor_gcs_service if user_type == UserType.DOCTOR else self.patient_gcs_service
		data = gcs_service.download_text(blob_name)
		return data
	
	def save_prompt_to_gcs(self, user_type, user_id, prompt_blob, prompt_data):
		blob_name = f"{user_id}/{prompt_blob}"
		gcs_service = self.doctor_gcs_service if user_type == UserType.DOCTOR else self.patient_gcs_service
		gcs_service.upload_text(blob_name, prompt_data)