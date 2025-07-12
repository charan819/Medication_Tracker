from flask import request, jsonify
from flask_restful import Resource
from flask_login import login_required, current_user
from marshmallow import ValidationError
from datetime import datetime

from database import db
from models import Reminder
from schemas import ReminderSchema

class ReminderListResource(Resource):
    @login_required
    def get(self):
        """Get all reminders for current user"""
        # Filter by type if provided
        reminder_type = request.args.get('type')
        is_active = request.args.get('active')
        
        query = Reminder.query.filter_by(user_id=current_user.id)
        
        if reminder_type:
            query = query.filter_by(reminder_type=reminder_type)
            
        if is_active is not None:
            is_active_bool = is_active.lower() in ['true', '1', 'yes']
            query = query.filter_by(is_active=is_active_bool)
            
        # Order by reminder time
        reminders = query.order_by(Reminder.reminder_time.asc()).all()
        
        reminder_schema = ReminderSchema(many=True)
        return reminder_schema.dump(reminders)
    
    @login_required
    def post(self):
        """Create a new reminder for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        try:
            reminder_schema = ReminderSchema()
            reminder = reminder_schema.load(json_data)
            reminder.user_id = current_user.id
            
            db.session.add(reminder)
            db.session.commit()
            return reminder_schema.dump(reminder), 201
                
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

class ReminderResource(Resource):
    @login_required
    def get(self, reminder_id):
        """Get a reminder by ID for current user"""
        reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first()
        
        if not reminder:
            return {'message': 'Reminder not found'}, 404
            
        reminder_schema = ReminderSchema()
        return reminder_schema.dump(reminder)
    
    @login_required
    def put(self, reminder_id):
        """Update a reminder for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first()
        
        if not reminder:
            return {'message': 'Reminder not found'}, 404
            
        try:
            reminder_schema = ReminderSchema(partial=True)
            reminder_data = reminder_schema.load(json_data, instance=reminder)
            
            db.session.commit()
            return reminder_schema.dump(reminder_data)
            
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @login_required
    def delete(self, reminder_id):
        """Delete a reminder for current user"""
        reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first()
        
        if not reminder:
            return {'message': 'Reminder not found'}, 404
            
        db.session.delete(reminder)
        db.session.commit()
        return '', 204