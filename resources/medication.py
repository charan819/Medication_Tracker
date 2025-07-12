from flask import request, jsonify
from flask_restful import Resource
from flask_login import login_required, current_user
from marshmallow import ValidationError
from datetime import datetime

from database import db
from models import Medication, MedicationLog
from schemas import MedicationSchema, MedicationLogSchema

class MedicationListResource(Resource):
    @login_required
    def get(self):
        """Get all medications for current user"""
        medications = Medication.query.filter_by(user_id=current_user.id).all()
        medication_schema = MedicationSchema(many=True)
        return medication_schema.dump(medications)
    
    @login_required
    def post(self):
        """Create a new medication for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        try:
            medication_schema = MedicationSchema()
            medication = medication_schema.load(json_data)
            medication.user_id = current_user.id
            
            db.session.add(medication)
            db.session.commit()
            return medication_schema.dump(medication), 201
                
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

class MedicationResource(Resource):
    @login_required
    def get(self, medication_id):
        """Get a medication by ID for current user"""
        medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
        
        if not medication:
            return {'message': 'Medication not found'}, 404
            
        medication_schema = MedicationSchema()
        return medication_schema.dump(medication)
    
    @login_required
    def put(self, medication_id):
        """Update a medication for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
        
        if not medication:
            return {'message': 'Medication not found'}, 404
            
        try:
            medication_schema = MedicationSchema(partial=True)
            medication_data = medication_schema.load(json_data, instance=medication)
            
            db.session.commit()
            return medication_schema.dump(medication_data)
            
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @login_required
    def delete(self, medication_id):
        """Delete a medication for current user"""
        medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
        
        if not medication:
            return {'message': 'Medication not found'}, 404
            
        db.session.delete(medication)
        db.session.commit()
        return '', 204

class MedicationLogResource(Resource):
    @login_required
    def get(self, medication_id):
        """Get medication logs for current user's medication"""
        medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
        
        if not medication:
            return {'message': 'Medication not found'}, 404
        
        logs = MedicationLog.query.filter_by(medication_id=medication_id, user_id=current_user.id).all()
        log_schema = MedicationLogSchema(many=True)
        return log_schema.dump(logs)
    
    @login_required
    def post(self, medication_id):
        """Create a medication log for current user's medication"""
        medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
        
        if not medication:
            return {'message': 'Medication not found'}, 404
        
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        try:
            log_schema = MedicationLogSchema()
            log = log_schema.load(json_data)
            log.medication_id = medication_id
            log.user_id = current_user.id
            
            db.session.add(log)
            db.session.commit()
            return log_schema.dump(log), 201
                
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

class MedicationStatusResource(Resource):
    @login_required
    def put(self, medication_id):
        """Update medication status for current user"""
        json_data = request.get_json()
        
        if not json_data or 'status' not in json_data:
            return {'message': 'Status is required'}, 400
            
        medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
        
        if not medication:
            return {'message': 'Medication not found'}, 404
            
        medication.status = json_data['status']
        db.session.commit()
        
        medication_schema = MedicationSchema()
        return medication_schema.dump(medication)