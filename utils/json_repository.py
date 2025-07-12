import logging
from datetime import datetime, date, time
from utils.data_loader import load_dummy_data, save_dummy_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JsonMedicationRepository:
    """Repository for medications using JSON file as data store."""
    
    @staticmethod
    def get_all():
        """Get all medications."""
        medications = load_dummy_data('medications')
        # Ensure we're working with a list
        return list(medications) if medications else []
    
    @staticmethod
    def get_by_id(medication_id):
        """Get a medication by ID."""
        medications = load_dummy_data('medications')
        for med in medications:
            if med['id'] == medication_id:
                return med
        return None
    
    @staticmethod
    def create(medication_data):
        """Create a new medication."""
        medications = list(load_dummy_data('medications'))
        
        # Generate new ID
        new_id = max([m['id'] for m in medications], default=0) + 1
        
        # Create new medication
        new_medication = {
            'id': new_id,
            'name': medication_data.get('name'),
            'dosage': medication_data.get('dosage'),
            'frequency': medication_data.get('frequency'),
            'intake_time': medication_data.get('intake_time'),
            'special_instructions': medication_data.get('special_instructions'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'logs': []
        }
        
        # Add to the list of medications
        medications.append(new_medication)
        save_dummy_data(medications, 'medications')
        
        return new_medication
    
    @staticmethod
    def update(medication_id, medication_data):
        """Update an existing medication."""
        medications = list(load_dummy_data('medications'))
        
        for i, med in enumerate(medications):
            if med['id'] == medication_id:
                # Update fields
                if 'name' in medication_data:
                    med['name'] = medication_data['name']
                if 'dosage' in medication_data:
                    med['dosage'] = medication_data['dosage']
                if 'frequency' in medication_data:
                    med['frequency'] = medication_data['frequency']
                if 'intake_time' in medication_data:
                    med['intake_time'] = medication_data['intake_time']
                if 'special_instructions' in medication_data:
                    med['special_instructions'] = medication_data['special_instructions']
                
                med['updated_at'] = datetime.utcnow()
                
                save_dummy_data(medications, 'medications')
                return med
                
        return None
    
    @staticmethod
    def delete(medication_id):
        """Delete a medication."""
        medications = list(load_dummy_data('medications'))
        
        for i, med in enumerate(medications):
            if med['id'] == medication_id:
                del medications[i]
                save_dummy_data(medications, 'medications')
                return True
                
        return False
    
    @staticmethod
    def add_log(medication_id, log_data):
        """Add a medication log."""
        medications = list(load_dummy_data('medications'))
        
        for med in medications:
            if med['id'] == medication_id:
                # Find all logs to generate a new ID
                all_logs = []
                for m in medications:
                    all_logs.extend(m['logs'])
                
                new_log_id = max([log['id'] for log in all_logs], default=0) + 1
                
                # Create new log
                new_log = {
                    'id': new_log_id,
                    'medication_id': medication_id,
                    'status': log_data.get('status', 'taken'),
                    'notes': log_data.get('notes'),
                    'taken_at': log_data.get('taken_at', datetime.utcnow())
                }
                
                med['logs'].append(new_log)
                save_dummy_data(medications, 'medications')
                
                return new_log
                
        return None

class JsonHealthMetricRepository:
    """Repository for health metrics using JSON file as data store."""
    
    @staticmethod
    def get_all(filters=None):
        """
        Get all health metrics with optional filtering.
        
        Args:
            filters (dict, optional): Filters to apply (metric_type, from_date, to_date).
        """
        metrics = list(load_dummy_data('health_metrics'))
        
        if not filters:
            return metrics
            
        filtered_metrics = metrics
        
        # Apply filters
        if 'metric_type' in filters and filters['metric_type']:
            filtered_metrics = [m for m in filtered_metrics if m['metric_type'] == filters['metric_type']]
            
        if 'from_date' in filters and filters['from_date']:
            from_date = filters['from_date']
            if isinstance(from_date, str):
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
            filtered_metrics = [m for m in filtered_metrics if m['recorded_at'] >= from_date]
            
        if 'to_date' in filters and filters['to_date']:
            to_date = filters['to_date']
            if isinstance(to_date, str):
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                to_date = datetime.combine(to_date.date(), datetime.max.time())
            filtered_metrics = [m for m in filtered_metrics if m['recorded_at'] <= to_date]
            
        # Sort by recorded_at in descending order
        filtered_metrics.sort(key=lambda x: x['recorded_at'], reverse=True)
        
        return filtered_metrics
    
    @staticmethod
    def get_by_id(metric_id):
        """Get a health metric by ID."""
        metrics = load_dummy_data('health_metrics')
        for metric in metrics:
            if metric['id'] == metric_id:
                return metric
        return None
    
    @staticmethod
    def create(metric_data):
        """Create a new health metric."""
        metrics = list(load_dummy_data('health_metrics'))
        
        # Generate new ID
        new_id = max([m['id'] for m in metrics], default=0) + 1
        
        # Handle blood pressure special case
        if metric_data.get('metric_type') == 'blood_pressure':
            systolic = metric_data.get('systolic')
            diastolic = metric_data.get('diastolic')
            value = metric_data.get('value', systolic)  # Use systolic as the primary value for graphing
        else:
            systolic = None
            diastolic = None
            value = metric_data.get('value')
            
        # Create new metric
        new_metric = {
            'id': new_id,
            'metric_type': metric_data.get('metric_type'),
            'value': value,
            'unit': metric_data.get('unit'),
            'notes': metric_data.get('notes'),
            'systolic': systolic,
            'diastolic': diastolic,
            'recorded_at': metric_data.get('recorded_at', datetime.utcnow())
        }
        
        metrics.append(new_metric)
        save_dummy_data(metrics, 'health_metrics')
        
        return new_metric
    
    @staticmethod
    def update(metric_id, metric_data):
        """Update an existing health metric."""
        metrics = list(load_dummy_data('health_metrics'))
        
        for i, metric in enumerate(metrics):
            if metric['id'] == metric_id:
                # Handle blood pressure special case
                if metric['metric_type'] == 'blood_pressure':
                    if 'systolic' in metric_data:
                        metric['systolic'] = metric_data['systolic']
                        # Update the primary value as well for graphing consistency
                        metric['value'] = metric_data['systolic']
                    if 'diastolic' in metric_data:
                        metric['diastolic'] = metric_data['diastolic']
                elif 'value' in metric_data:
                    metric['value'] = metric_data['value']
                
                # Update other fields
                if 'unit' in metric_data:
                    metric['unit'] = metric_data['unit']
                if 'notes' in metric_data:
                    metric['notes'] = metric_data['notes']
                
                save_dummy_data(metrics, 'health_metrics')
                return metric
                
        return None
    
    @staticmethod
    def delete(metric_id):
        """Delete a health metric."""
        metrics = list(load_dummy_data('health_metrics'))
        
        for i, metric in enumerate(metrics):
            if metric['id'] == metric_id:
                del metrics[i]
                save_dummy_data(metrics, 'health_metrics')
                return True
                
        return False

class JsonAppointmentRepository:
    """Repository for appointments using JSON file as data store."""
    
    @staticmethod
    def get_all(filters=None):
        """
        Get all appointments with optional filtering.
        
        Args:
            filters (dict, optional): Filters to apply (status, from_date, to_date).
        """
        appointments = list(load_dummy_data('appointments'))
        
        if not filters:
            return appointments
            
        filtered_appointments = appointments
        
        # Apply filters
        if 'status' in filters and filters['status']:
            filtered_appointments = [a for a in filtered_appointments if a['status'] == filters['status']]
            
        if 'from_date' in filters and filters['from_date']:
            from_date = filters['from_date']
            if isinstance(from_date, str):
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            filtered_appointments = [a for a in filtered_appointments if a['date'] >= from_date]
            
        if 'to_date' in filters and filters['to_date']:
            to_date = filters['to_date']
            if isinstance(to_date, str):
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            filtered_appointments = [a for a in filtered_appointments if a['date'] <= to_date]
            
        # Sort by date and time
        filtered_appointments.sort(key=lambda x: (x['date'], x['time']))
        
        return filtered_appointments
    
    @staticmethod
    def get_by_id(appointment_id):
        """Get an appointment by ID."""
        appointments = load_dummy_data('appointments')
        for appointment in appointments:
            if appointment['id'] == appointment_id:
                return appointment
        return None
    
    @staticmethod
    def create(appointment_data):
        """Create a new appointment."""
        appointments = list(load_dummy_data('appointments'))
        
        # Generate new ID
        new_id = max([a['id'] for a in appointments], default=0) + 1
        
        # Handle date and time conversion
        appt_date = appointment_data.get('date')
        if isinstance(appt_date, str):
            appt_date = date.fromisoformat(appt_date)
            
        appt_time = appointment_data.get('time')
        if isinstance(appt_time, str):
            appt_time = time.fromisoformat(appt_time)
        
        # Create new appointment
        new_appointment = {
            'id': new_id,
            'title': appointment_data.get('title'),
            'doctor_name': appointment_data.get('doctor_name'),
            'hospital_name': appointment_data.get('hospital_name'),
            'date': appt_date,
            'time': appt_time,
            'location': appointment_data.get('location'),
            'notes': appointment_data.get('notes'),
            'status': appointment_data.get('status', 'scheduled'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        appointments.append(new_appointment)
        save_dummy_data(appointments, 'appointments')
        
        return new_appointment
    
    @staticmethod
    def update(appointment_id, appointment_data):
        """Update an existing appointment."""
        appointments = list(load_dummy_data('appointments'))
        
        for i, appointment in enumerate(appointments):
            if appointment['id'] == appointment_id:
                # Handle date and time conversion
                if 'date' in appointment_data:
                    appt_date = appointment_data['date']
                    if isinstance(appt_date, str):
                        appt_date = date.fromisoformat(appt_date)
                    appointment['date'] = appt_date
                    
                if 'time' in appointment_data:
                    appt_time = appointment_data['time']
                    if isinstance(appt_time, str):
                        appt_time = time.fromisoformat(appt_time)
                    appointment['time'] = appt_time
                
                # Update other fields
                if 'title' in appointment_data:
                    appointment['title'] = appointment_data['title']
                if 'doctor_name' in appointment_data:
                    appointment['doctor_name'] = appointment_data['doctor_name']
                if 'hospital_name' in appointment_data:
                    appointment['hospital_name'] = appointment_data['hospital_name']
                if 'location' in appointment_data:
                    appointment['location'] = appointment_data['location']
                if 'notes' in appointment_data:
                    appointment['notes'] = appointment_data['notes']
                
                appointment['updated_at'] = datetime.utcnow()
                
                save_dummy_data(appointments, 'appointments')
                return appointment
                
        return None
    
    @staticmethod
    def update_status(appointment_id, status):
        """Update an appointment's status."""
        appointments = list(load_dummy_data('appointments'))
        
        for appointment in appointments:
            if appointment['id'] == appointment_id:
                appointment['status'] = status
                appointment['updated_at'] = datetime.utcnow()
                
                save_dummy_data(appointments, 'appointments')
                return appointment
                
        return None
    
    @staticmethod
    def delete(appointment_id):
        """Delete an appointment."""
        appointments = list(load_dummy_data('appointments'))
        
        for i, appointment in enumerate(appointments):
            if appointment['id'] == appointment_id:
                del appointments[i]
                save_dummy_data(appointments, 'appointments')
                return True
                
        return False

class JsonReminderRepository:
    """Repository for reminders using JSON file as data store."""
    
    @staticmethod
    def get_all(filters=None):
        """
        Get all reminders with optional filtering.
        
        Args:
            filters (dict, optional): Filters to apply (reminder_type, is_active, from_time, to_time).
        """
        reminders = list(load_dummy_data('reminders'))
        
        if not filters:
            return reminders
            
        filtered_reminders = reminders
        
        # Apply filters
        if 'reminder_type' in filters and filters['reminder_type']:
            filtered_reminders = [r for r in filtered_reminders if r['reminder_type'] == filters['reminder_type']]
            
        if 'is_active' in filters and filters['is_active'] is not None:
            is_active_bool = filters['is_active']
            if isinstance(is_active_bool, str):
                is_active_bool = is_active_bool.lower() == 'true'
            filtered_reminders = [r for r in filtered_reminders if r['is_active'] == is_active_bool]
            
        if 'from_time' in filters and filters['from_time']:
            from_time = filters['from_time']
            if isinstance(from_time, str):
                from_time = datetime.fromisoformat(from_time)
            filtered_reminders = [r for r in filtered_reminders if r['reminder_time'] >= from_time]
            
        if 'to_time' in filters and filters['to_time']:
            to_time = filters['to_time']
            if isinstance(to_time, str):
                to_time = datetime.fromisoformat(to_time)
            filtered_reminders = [r for r in filtered_reminders if r['reminder_time'] <= to_time]
            
        # Sort by reminder_time
        filtered_reminders.sort(key=lambda x: x['reminder_time'])
        
        return filtered_reminders
    
    @staticmethod
    def get_by_id(reminder_id):
        """Get a reminder by ID."""
        reminders = load_dummy_data('reminders')
        for reminder in reminders:
            if reminder['id'] == reminder_id:
                return reminder
        return None
    
    @staticmethod
    def create(reminder_data):
        """Create a new reminder."""
        reminders = list(load_dummy_data('reminders'))
        
        # Generate new ID
        new_id = max([r['id'] for r in reminders], default=0) + 1
        
        # Handle reminder_time conversion
        reminder_time = reminder_data.get('reminder_time')
        if isinstance(reminder_time, str):
            reminder_time = datetime.fromisoformat(reminder_time)
        
        # Create new reminder
        new_reminder = {
            'id': new_id,
            'reminder_type': reminder_data.get('reminder_type'),
            'target_id': reminder_data.get('target_id'),
            'title': reminder_data.get('title'),
            'message': reminder_data.get('message'),
            'reminder_time': reminder_time,
            'repeat_interval': reminder_data.get('repeat_interval', 'once'),
            'is_active': reminder_data.get('is_active', True),
            'notification_method': reminder_data.get('notification_method', 'app'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        reminders.append(new_reminder)
        save_dummy_data(reminders, 'reminders')
        
        return new_reminder
    
    @staticmethod
    def update(reminder_id, reminder_data):
        """Update an existing reminder."""
        reminders = list(load_dummy_data('reminders'))
        
        for reminder in reminders:
            if reminder['id'] == reminder_id:
                # Handle reminder_time conversion
                if 'reminder_time' in reminder_data:
                    reminder_time = reminder_data['reminder_time']
                    if isinstance(reminder_time, str):
                        reminder_time = datetime.fromisoformat(reminder_time)
                    reminder['reminder_time'] = reminder_time
                
                # Update other fields
                if 'title' in reminder_data:
                    reminder['title'] = reminder_data['title']
                if 'message' in reminder_data:
                    reminder['message'] = reminder_data['message']
                if 'repeat_interval' in reminder_data:
                    reminder['repeat_interval'] = reminder_data['repeat_interval']
                if 'is_active' in reminder_data:
                    reminder['is_active'] = reminder_data['is_active']
                if 'notification_method' in reminder_data:
                    reminder['notification_method'] = reminder_data['notification_method']
                
                reminder['updated_at'] = datetime.utcnow()
                
                save_dummy_data(reminders, 'reminders')
                return reminder
                
        return None
    
    @staticmethod
    def delete(reminder_id):
        """Delete a reminder."""
        reminders = list(load_dummy_data('reminders'))
        
        for i, reminder in enumerate(reminders):
            if reminder['id'] == reminder_id:
                del reminders[i]
                save_dummy_data(reminders, 'reminders')
                return True
                
        return False