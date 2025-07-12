from flask import request, jsonify
from flask_restful import Resource
from flask_login import login_required, current_user
from marshmallow import ValidationError
from datetime import datetime

from database import db
from models import HealthMetric
from schemas import HealthMetricSchema

class HealthMetricListResource(Resource):
    @login_required
    def get(self):
        """Get all health metrics for current user"""
        # Filter by metric type if provided
        metric_type = request.args.get('type')
        
        query = HealthMetric.query.filter_by(user_id=current_user.id)
        
        if metric_type:
            query = query.filter_by(metric_type=metric_type)
            
        # Order by most recent first
        metrics = query.order_by(HealthMetric.recorded_at.desc()).all()
        
        metric_schema = HealthMetricSchema(many=True)
        return metric_schema.dump(metrics)
    
    @login_required
    def post(self):
        """Create a new health metric for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        try:
            metric_schema = HealthMetricSchema()
            metric = metric_schema.load(json_data)
            metric.user_id = current_user.id
            
            db.session.add(metric)
            db.session.commit()
            return metric_schema.dump(metric), 201
                
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500

class HealthMetricResource(Resource):
    @login_required
    def get(self, metric_id):
        """Get a health metric by ID for current user"""
        metric = HealthMetric.query.filter_by(id=metric_id, user_id=current_user.id).first()
        
        if not metric:
            return {'message': 'Health metric not found'}, 404
            
        metric_schema = HealthMetricSchema()
        return metric_schema.dump(metric)
    
    @login_required
    def put(self, metric_id):
        """Update a health metric for current user"""
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
            
        metric = HealthMetric.query.filter_by(id=metric_id, user_id=current_user.id).first()
        
        if not metric:
            return {'message': 'Health metric not found'}, 404
            
        try:
            metric_schema = HealthMetricSchema(partial=True)
            metric_data = metric_schema.load(json_data, instance=metric)
            
            db.session.commit()
            return metric_schema.dump(metric_data)
            
        except ValidationError as err:
            return {'message': err.messages}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @login_required
    def delete(self, metric_id):
        """Delete a health metric for current user"""
        metric = HealthMetric.query.filter_by(id=metric_id, user_id=current_user.id).first()
        
        if not metric:
            return {'message': 'Health metric not found'}, 404
            
        db.session.delete(metric)
        db.session.commit()
        return '', 204