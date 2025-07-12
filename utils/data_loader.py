import json
import os
import logging
from datetime import datetime, date, time

def load_dummy_data(data_type=None):
    """
    Load dummy data from the JSON file.
    
    Args:
        data_type (str, optional): Type of data to load ('medications', 'health_metrics', 
                                 'appointments', or 'reminders'). 
                                 If None, returns all data.
    
    Returns:
        dict or list: The loaded dummy data.
    """
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dummy_data.json')
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Parse dates and times if needed
        if data_type == 'medications' or data_type is None:
            for medication in data['medications']:
                medication['created_at'] = datetime.fromisoformat(medication['created_at'])
                medication['updated_at'] = datetime.fromisoformat(medication['updated_at'])
                for log in medication['logs']:
                    log['taken_at'] = datetime.fromisoformat(log['taken_at'])
        
        if data_type == 'health_metrics' or data_type is None:
            for metric in data['health_metrics']:
                metric['recorded_at'] = datetime.fromisoformat(metric['recorded_at'])
        
        if data_type == 'appointments' or data_type is None:
            for appointment in data['appointments']:
                appointment['date'] = date.fromisoformat(appointment['date'])
                appointment['time'] = time.fromisoformat(appointment['time'])
                appointment['created_at'] = datetime.fromisoformat(appointment['created_at'])
                appointment['updated_at'] = datetime.fromisoformat(appointment['updated_at'])
        
        if data_type == 'reminders' or data_type is None:
            for reminder in data['reminders']:
                reminder['reminder_time'] = datetime.fromisoformat(reminder['reminder_time'])
                reminder['created_at'] = datetime.fromisoformat(reminder['created_at'])
                reminder['updated_at'] = datetime.fromisoformat(reminder['updated_at'])
        
        if data_type:
            # Ensure we return a list for array data types
            return list(data[data_type]) if data_type in data else []
        else:
            # Return the whole data dictionary
            return data
            
    except Exception as e:
        logging.error(f"Error loading dummy data: {str(e)}")
        return [] if data_type else {}

def save_dummy_data(data, data_type=None):
    """
    Save data to the dummy data JSON file.
    
    Args:
        data (dict or list): The data to save.
        data_type (str, optional): Type of data to save ('medications', 'health_metrics', 
                                 'appointments', or 'reminders'). 
                                 If None, assumes data is the complete dataset.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dummy_data.json')
        
        # Convert datetime objects to strings
        if data_type:
            # Load existing data
            with open(file_path, 'r') as file:
                full_data = json.load(file)
            
            # Update specific data type
            full_data[data_type] = _convert_datetime_to_str(data)
        else:
            # Full data replacement
            full_data = _convert_datetime_to_str(data)
        
        # Write back to file
        with open(file_path, 'w') as file:
            json.dump(full_data, file, indent=2)
        
        return True
            
    except Exception as e:
        logging.error(f"Error saving dummy data: {str(e)}")
        return False

def _convert_datetime_to_str(data):
    """
    Convert datetime, date, and time objects to strings for JSON serialization.
    
    Args:
        data: The data to convert.
    
    Returns:
        The data with datetime objects converted to strings.
    """
    if isinstance(data, dict):
        return {k: _convert_datetime_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_convert_datetime_to_str(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, date):
        return data.isoformat()
    elif isinstance(data, time):
        return data.isoformat()
    else:
        return data