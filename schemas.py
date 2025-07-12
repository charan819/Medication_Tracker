from marshmallow import Schema, fields, validate, ValidationError, validates, validates_schema
from database import ma
from models import Medication, MedicationLog, HealthMetric, Appointment, Reminder

# Medication Log Schema
class MedicationLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MedicationLog
        include_fk = True
        load_instance = True
        
    status = fields.String(validate=validate.OneOf(['taken', 'skipped', 'missed']))

# Medication Schema
class MedicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Medication
        include_relationships = True
        load_instance = True
        
    logs = fields.List(fields.Nested(MedicationLogSchema), dump_only=True)
    
    @validates('frequency')
    def validate_frequency(self, value, **kwargs):
        valid_frequencies = ['once_daily', 'twice_daily', 'three_times_daily', 'four_times_daily', 'as_needed', 'weekly', 'monthly']
        if value not in valid_frequencies and not value.startswith('custom:'):
            raise ValidationError(f"Invalid frequency. Must be one of {valid_frequencies} or start with 'custom:'")

# Health Metric Schema
class HealthMetricSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HealthMetric
        load_instance = True
        
    metric_type = fields.String(validate=validate.OneOf(['blood_pressure', 'glucose', 'weight', 'temperature', 'heart_rate', 'oxygen', 'mood', 'symptoms', 'other']))
    
    @validates_schema
    def validate_blood_pressure(self, data, **kwargs):
        if data.get('metric_type') == 'blood_pressure':
            if 'systolic' not in data or 'diastolic' not in data:
                raise ValidationError("Blood pressure requires both systolic and diastolic values")

# Appointment Schema
class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True
        
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    status = fields.String(validate=validate.OneOf(['scheduled', 'completed', 'missed', 'cancelled']))

# Reminder Schema
class ReminderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reminder
        load_instance = True
        
    reminder_type = fields.String(validate=validate.OneOf(['medication', 'appointment', 'health_check']))
    notification_method = fields.String(validate=validate.OneOf(['app', 'email', 'sms']))
    repeat_interval = fields.String(validate=validate.OneOf(['once', 'daily', 'weekly', 'monthly', 'custom']))
