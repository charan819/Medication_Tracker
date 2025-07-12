import os
import sys
import logging
from datetime import datetime, date, time
from app import app, db
from models import Medication, MedicationLog, HealthMetric, Appointment, Reminder
from utils.data_loader import load_dummy_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def seed_medications():
    """Seed the medications table with dummy data."""
    try:
        logger.info("Seeding medications table...")
        medications_data = load_dummy_data('medications')
        
        for med_data in medications_data:
            # Check if medication already exists
            existing = Medication.query.filter_by(id=med_data['id']).first()
            if existing:
                logger.info(f"Medication {med_data['name']} already exists, skipping.")
                continue
                
            # Create medication
            medication = Medication(
                id=med_data['id'],
                name=med_data['name'],
                dosage=med_data['dosage'],
                frequency=med_data['frequency'],
                intake_time=med_data['intake_time'],
                special_instructions=med_data['special_instructions'],
                created_at=datetime.fromisoformat(med_data['created_at']) if isinstance(med_data['created_at'], str) else med_data['created_at'],
                updated_at=datetime.fromisoformat(med_data['updated_at']) if isinstance(med_data['updated_at'], str) else med_data['updated_at']
            )
            db.session.add(medication)
            
            # Add medication logs
            for log_data in med_data['logs']:
                log = MedicationLog(
                    id=log_data['id'],
                    medication_id=log_data['medication_id'],
                    status=log_data['status'],
                    notes=log_data['notes'],
                    taken_at=datetime.fromisoformat(log_data['taken_at']) if isinstance(log_data['taken_at'], str) else log_data['taken_at']
                )
                db.session.add(log)
                
        db.session.commit()
        logger.info("Medications seeded successfully.")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error seeding medications: {str(e)}")

def seed_health_metrics():
    """Seed the health metrics table with dummy data."""
    try:
        logger.info("Seeding health metrics table...")
        metrics_data = load_dummy_data('health_metrics')
        
        for metric_data in metrics_data:
            # Check if health metric already exists
            existing = HealthMetric.query.filter_by(id=metric_data['id']).first()
            if existing:
                logger.info(f"Health metric ID {metric_data['id']} already exists, skipping.")
                continue
                
            # Create health metric
            metric = HealthMetric(
                id=metric_data['id'],
                metric_type=metric_data['metric_type'],
                value=metric_data['value'],
                unit=metric_data['unit'],
                notes=metric_data['notes'],
                systolic=metric_data['systolic'],
                diastolic=metric_data['diastolic'],
                recorded_at=datetime.fromisoformat(metric_data['recorded_at']) if isinstance(metric_data['recorded_at'], str) else metric_data['recorded_at']
            )
            db.session.add(metric)
                
        db.session.commit()
        logger.info("Health metrics seeded successfully.")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error seeding health metrics: {str(e)}")

def seed_appointments():
    """Seed the appointments table with dummy data."""
    try:
        logger.info("Seeding appointments table...")
        appointments_data = load_dummy_data('appointments')
        
        for appt_data in appointments_data:
            # Check if appointment already exists
            existing = Appointment.query.filter_by(id=appt_data['id']).first()
            if existing:
                logger.info(f"Appointment ID {appt_data['id']} already exists, skipping.")
                continue
                
            # Convert date and time if they're strings
            appt_date = date.fromisoformat(appt_data['date']) if isinstance(appt_data['date'], str) else appt_data['date']
            appt_time = time.fromisoformat(appt_data['time']) if isinstance(appt_data['time'], str) else appt_data['time']
            
            # Create appointment
            appointment = Appointment(
                id=appt_data['id'],
                title=appt_data['title'],
                doctor_name=appt_data['doctor_name'],
                hospital_name=appt_data['hospital_name'],
                date=appt_date,
                time=appt_time,
                location=appt_data['location'],
                notes=appt_data['notes'],
                status=appt_data['status'],
                created_at=datetime.fromisoformat(appt_data['created_at']) if isinstance(appt_data['created_at'], str) else appt_data['created_at'],
                updated_at=datetime.fromisoformat(appt_data['updated_at']) if isinstance(appt_data['updated_at'], str) else appt_data['updated_at']
            )
            db.session.add(appointment)
                
        db.session.commit()
        logger.info("Appointments seeded successfully.")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error seeding appointments: {str(e)}")

def seed_reminders():
    """Seed the reminders table with dummy data."""
    try:
        logger.info("Seeding reminders table...")
        reminders_data = load_dummy_data('reminders')
        
        for reminder_data in reminders_data:
            # Check if reminder already exists
            existing = Reminder.query.filter_by(id=reminder_data['id']).first()
            if existing:
                logger.info(f"Reminder ID {reminder_data['id']} already exists, skipping.")
                continue
                
            # Create reminder
            reminder = Reminder(
                id=reminder_data['id'],
                reminder_type=reminder_data['reminder_type'],
                target_id=reminder_data['target_id'],
                title=reminder_data['title'],
                message=reminder_data['message'],
                reminder_time=datetime.fromisoformat(reminder_data['reminder_time']) if isinstance(reminder_data['reminder_time'], str) else reminder_data['reminder_time'],
                repeat_interval=reminder_data['repeat_interval'],
                is_active=reminder_data['is_active'],
                notification_method=reminder_data['notification_method'],
                created_at=datetime.fromisoformat(reminder_data['created_at']) if isinstance(reminder_data['created_at'], str) else reminder_data['created_at'],
                updated_at=datetime.fromisoformat(reminder_data['updated_at']) if isinstance(reminder_data['updated_at'], str) else reminder_data['updated_at']
            )
            db.session.add(reminder)
                
        db.session.commit()
        logger.info("Reminders seeded successfully.")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error seeding reminders: {str(e)}")

def seed_all():
    """Seed all tables with dummy data."""
    with app.app_context():
        # Clear existing data (optional)
        logger.info("Clearing existing data...")
        MedicationLog.query.delete()
        Medication.query.delete()
        HealthMetric.query.delete()
        Appointment.query.delete()
        Reminder.query.delete()
        db.session.commit()
        
        # Seed tables
        seed_medications()
        seed_health_metrics()
        seed_appointments()
        seed_reminders()
        
        logger.info("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_all()