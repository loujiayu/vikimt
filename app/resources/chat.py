from flask_restful import Resource
from flask_login import login_user, logout_user, login_required
from flask import jsonify, request
import logging
from app.gcs_service import GCSService
from app.ai_services import get_ai_service

class ChatAPI(Resource):
	def __init__(self):
		self.gcs_service = GCSService("patientstorage")
		self.ai_service = get_ai_service()  # Get default AI service

	@login_required
	def post(self, patient_id):
		try:
			data = request.get_json()
			messages = data.get("messages", [])

			if not messages:
				return {"error": "No messages provided"}, 400
			
			# Fetch system_instruction from Google Cloud Storage
			system_instruction_blob = f"{patient_id}/system_instruction.txt"
			system_instruction = self.gcs_service.download_text(system_instruction_blob)
			if not system_instruction:
				system_instruction = "You are a helpful assistant."
			
			logging.info(f"System instruction: {system_instruction}")

			# Use the AI service to generate a response
			response_text = ""
			logging.info("start generate_content_stream")
			for chunk in self.ai_service.generate_stream(messages, system_instruction):
				logging.info(chunk)
				response_text += chunk

			return {'message': response_text}, 201

		except Exception as e:
			return {"error": str(e)}, 500