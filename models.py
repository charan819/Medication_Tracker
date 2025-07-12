from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# User Model for Authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

# Medication Model
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    intake_time = db.Column(db.String(100), nullable=False)  # Store as string like "08:00, 14:00, 20:00"
    special_instructions = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active')  # 'active', 'inactive', 'discontinued'
    notes = db.Column(db.Text, nullable=True)  # General notes about the medication
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to medication logs
    logs = db.relationship('MedicationLog', backref='medication', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Medication {self.name}>'

# Medication Log Model
class MedicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='taken')  # 'taken', 'skipped', 'missed'
    notes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<MedicationLog {self.medication_id} - {self.taken_at}>'

# Health Metric Model
class HealthMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # 'blood_pressure', 'glucose', 'weight', etc.
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # 'mmHg', 'mg/dL', 'kg', etc.
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    
    # For blood pressure, we might need additional fields
    systolic = db.Column(db.Float, nullable=True)  # Only for blood pressure
    diastolic = db.Column(db.Float, nullable=True)  # Only for blood pressure
    
    def __repr__(self):
        return f'<HealthMetric {self.metric_type} - {self.value} {self.unit}>'

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=True)
    hospital_name = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='scheduled')  # 'scheduled', 'completed', 'missed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.title} - {self.date}>'

# Reminder Model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reminder_type = db.Column(db.String(20), nullable=False)  # 'medication', 'appointment', 'health_check'
    target_id = db.Column(db.Integer, nullable=True)  # ID of the medication, appointment, etc.
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    repeat_interval = db.Column(db.String(20), nullable=True)  # 'daily', 'weekly', 'monthly', etc.
    is_active = db.Column(db.Boolean, default=True)
    notification_method = db.Column(db.String(20), default='app')  # 'app', 'email', 'sms'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reminder {self.title} - {self.reminder_time}>'
