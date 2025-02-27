from flask_restful import Resource
from flask import jsonify
from app import db
from app.models.patient import Patient
from app.decorators import doctor_required

class PatientsResource(Resource):
    @doctor_required
    def get(self):
        try:
            # Get top 20 patients, ordered by most recently updated
            patients = Patient.query.order_by(Patient.updated_at.desc()).limit(20).all()
            
            # Convert to JSON serializable format
            patients_data = []
            for patient in patients:
                patients_data.append({
                    'patient_id': patient.patient_id,
                    'full_name': patient.full_name,
                    'email': patient.email,
                    'metadata': patient.patient_metadata,
                    'created_at': patient.created_at.isoformat() if patient.created_at else None,
                    'updated_at': patient.updated_at.isoformat() if patient.updated_at else None
                })
            
            return jsonify(patients_data)
        
        except Exception as e:
            return {'error': str(e)}, 500
