from datetime import datetime, date, time
import os

def parse_date(date_str):
    """
    Parse a date string in ISO format (YYYY-MM-DD).
    
    Args:
        date_str (str): Date string in ISO format.
        
    Returns:
        date: Parsed date object, or None if parsing fails.
    """
    if not date_str:
        return None
        
    try:
        return date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None

def parse_time(time_str):
    """
    Parse a time string in ISO format (HH:MM or HH:MM:SS).
    
    Args:
        time_str (str): Time string in ISO format.
        
    Returns:
        time: Parsed time object, or None if parsing fails.
    """
    if not time_str:
        return None
        
    try:
        return time.fromisoformat(time_str)
    except (ValueError, TypeError):
        return None

def parse_datetime(datetime_str):
    """
    Parse a datetime string in ISO format.
    
    Args:
        datetime_str (str): Datetime string in ISO format.
        
    Returns:
        datetime: Parsed datetime object, or None if parsing fails.
    """
    if not datetime_str:
        return None
        
    try:
        return datetime.fromisoformat(datetime_str)
    except (ValueError, TypeError):
        return None

def is_valid_json_data_source():
    """
    Check if the dummy data JSON file exists and is valid.
    
    Returns:
        bool: True if the file exists and is valid, False otherwise.
    """
    try:
        from utils.data_loader import load_dummy_data
        data = load_dummy_data()
        return (
            'medications' in data and
            'health_metrics' in data and
            'appointments' in data and
            'reminders' in data
        )
    except Exception:
        return False

def should_use_json_repository():
    """
    Determine if the application should use the JSON repository instead of the database.
    
    Returns:
        bool: True if the JSON repository should be used, False otherwise.
    """
    # Check for environment variable that can override the default behavior
    use_json = os.environ.get('USE_JSON_REPOSITORY', '').lower() == 'true'
    
    # If the environment variable is set, use its value
    if 'USE_JSON_REPOSITORY' in os.environ:
        return use_json
        
    # Otherwise, check if the database is available
    try:
        from app import db
        db.engine.execute('SELECT 1')
        return False  # Database is available, use it
    except Exception:
        # Database is not available, check if the JSON file is valid
        return is_valid_json_data_source()

def get_repository(repository_type):
    """
    Get the appropriate repository implementation based on configuration.
    
    Args:
        repository_type (str): Type of repository ('medication', 'health_metric', 'appointment', 'reminder').
        
    Returns:
        object: Repository implementation.
    """
    if should_use_json_repository():
        if repository_type == 'medication':
            from utils.json_repository import JsonMedicationRepository
            return JsonMedicationRepository
        elif repository_type == 'health_metric':
            from utils.json_repository import JsonHealthMetricRepository
            return JsonHealthMetricRepository
        elif repository_type == 'appointment':
            from utils.json_repository import JsonAppointmentRepository
            return JsonAppointmentRepository
        elif repository_type == 'reminder':
            from utils.json_repository import JsonReminderRepository
            return JsonReminderRepository
    else:
        # Return None to indicate that the database models should be used directly
        return None