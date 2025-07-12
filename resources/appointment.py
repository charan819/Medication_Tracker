from flask import request, jsonify
from flask_restful import Resource
from flask_login import login_required, current_user
from marshmallow import ValidationError
from datetime import datetime, date

from database import db
from models import Appointment
from schemas import AppointmentSchema

class AppointmentListResource(Resource):
    @login_required
    def get(self):
        """Get all appointments for current user"""
        # Filter by status if provided
        status = request.args.get('status')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        
        query = Appointment.query.filter_by(user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
            
        if from_date:
            try:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                query = query.filter(Appointment.date >= from_date_obj)
            except ValueError:
                return {'message': 'Invalid from_date format. Use YYYY-MM-DD'}, 400
                
        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                query = query.filter(Appointment.date <= to_date_obj)
            except ValueError:
                return {'message': 'Invalid to_date format. Use YYYY-MM-DD'}, 400
            
        # Order by date and time
        appointments = query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()
        
        appointment_schema = AppointmentSchema(many=True)
        return appointment_schema.dump(appointments)
    
    @login_required
    def post(self):
        """Create a new appointment for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        try:
            appointment_schema = AppointmentSchema()
            appointment = appointment_schema.load(json_data)
            appointment.user_id = current_user.id
            
            db.session.add(appointment)
            db.session.commit()
            return appointment_schema.dump(appointment), 201
                
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

class AppointmentResource(Resource):
    @login_required
    def get(self, appointment_id):
        """Get an appointment by ID for current user"""
        appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first()
        
        if not appointment:
            return {'message': 'Appointment not found'}, 404
            
        appointment_schema = AppointmentSchema()
        return appointment_schema.dump(appointment)
    
    @login_required
    def put(self, appointment_id):
        """Update an appointment for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first()
        
        if not appointment:
            return {'message': 'Appointment not found'}, 404
            
        try:
            appointment_schema = AppointmentSchema(partial=True)
            appointment_data = appointment_schema.load(json_data, instance=appointment)
            
            db.session.commit()
            return appointment_schema.dump(appointment_data)
            
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @login_required
    def delete(self, appointment_id):
        """Delete an appointment for current user"""
        appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first()
        
        if not appointment:
            return {'message': 'Appointment not found'}, 404
            
        db.session.delete(appointment)
        db.session.commit()
        return '', 204

class AppointmentStatusResource(Resource):
    @login_required
    def put(self, appointment_id):
        """Update appointment status for current user"""
        json_data = request.get_json()
        
        if not json_data or 'status' not in json_data:
            return {'message': 'Status is required'}, 400
            
        appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first()
        
        if not appointment:
            return {'message': 'Appointment not found'}, 404
            
        appointment.status = json_data['status']
        db.session.commit()
        
        appointment_schema = AppointmentSchema()
        return appointment_schema.dump(appointment)