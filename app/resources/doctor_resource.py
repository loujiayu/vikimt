from flask_restful import Resource
from flask import request, jsonify
from flask_login import login_required, current_user
from app.models.doctor import Doctor
from app.decorators import doctor_required
import logging

class DoctorResource(Resource):
    """Resource for doctor-related operations."""
    
    @login_required
    def get(self, doctor_id=None):
        """
        Get doctor information by ID.
        
        Args:
            doctor_id: The ID of the doctor to retrieve. If None, returns current doctor.
        
        Returns:
            Doctor information as JSON
        """
        try:
            # Check if requesting current doctor's information
            if doctor_id is None and hasattr(current_user, 'doctor_id'):
                doctor_id = current_user.doctor_id
            
            # If still no doctor_id, return error
            if doctor_id is None:
                return {"error": "Doctor ID is required"}, 400
            
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return {"error": f"Doctor with ID {doctor_id} not found"}, 404
            
            # Build doctor data response
            doctor_data = {
                "doctor_id": doctor.doctor_id,
                "full_name": doctor.full_name,
                "email": doctor.email,
                "sso_provider": doctor.sso_provider,
                "created_at": doctor.created_at.isoformat() if doctor.created_at else None,
                "updated_at": doctor.updated_at.isoformat() if doctor.updated_at else None
            }
            
            return doctor_data, 200
            
        except Exception as e:
            logging.error(f"Error retrieving doctor: {str(e)}")
            return {"error": "Failed to retrieve doctor information"}, 500
