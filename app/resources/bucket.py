from flask_restful import Resource
from flask import jsonify
from google.cloud import storage
from flask_login import login_user, logout_user, login_required
from app.gcs_service import GCSService

class ChatHistoryResource(Resource):
	GCS_BUCKET_NAME = "patientstorage"
	def __init__(self):
		self.gcs_service = GCSService(self.GCS_BUCKET_NAME)
		
	@login_required
	def get(self, patient_id):
		chat_history = self.get_chat_history_from_gcs(patient_id)
		if not chat_history:
				return {'message': 'No chat history found for this patient.'}, 404
		
		return jsonify(chat_history)

	def get_chat_history_from_gcs(self, patient_id):
		blob_name = f"{patient_id}/patient"
		data =self.gcs_service.download_text(blob_name)
		return data
