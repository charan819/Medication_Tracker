// Main JavaScript for Health Management App

// Helper function to show an alert message
function showAlert(message, type = 'success', timeout = 5000) {
    // Create alert container if not exists
    let alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.id = 'alert-container';
        alertContainer.style.position = 'fixed';
        alertContainer.style.top = '20px';
        alertContainer.style.right = '20px';
        alertContainer.style.zIndex = '9999';
        document.body.appendChild(alertContainer);
    }

    // Create the alert element
    const alertEl = document.createElement('div');
    alertEl.className = `alert alert-${type} alert-dismissible fade show`;
    alertEl.role = 'alert';
    alertEl.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Add the alert to the container
    alertContainer.appendChild(alertEl);

    // Set timeout to remove the alert
    setTimeout(() => {
        if (alertEl) {
            alertEl.classList.remove('show');
            setTimeout(() => alertEl.remove(), 150);
        }
    }, timeout);
}

// Generic error handler for fetch requests
function handleFetchError(error) {
    console.error('Fetch error:', error);
    showAlert('Error: Could not complete the request. Please try again later.', 'danger');
}

// Function to format a date string
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Function to format a time string
function formatTime(timeString) {
    if (!timeString) return '';
    
    // Handle ISO time strings
    if (timeString.includes('T')) {
        const date = new Date(timeString);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    // Handle HH:MM:SS time strings
    const timeParts = timeString.split(':');
    if (timeParts.length >= 2) {
        const hours = parseInt(timeParts[0]);
        const minutes = parseInt(timeParts[1]);
        
        const period = hours >= 12 ? 'PM' : 'AM';
        const hour12 = hours % 12 === 0 ? 12 : hours % 12;
        
        return `${hour12}:${minutes.toString().padStart(2, '0')} ${period}`;
    }
    
    return timeString;
}

// Function to show a loading spinner
function showLoader() {
    const loaders = document.querySelectorAll('.loader');
    loaders.forEach(loader => {
        loader.style.display = 'block';
    });
}

// Function to hide a loading spinner
function hideLoader() {
    const loaders = document.querySelectorAll('.loader');
    loaders.forEach(loader => {
        loader.style.display = 'none';
    });
}

// API Helper functions

// Get all medications
async function fetchMedications() {
    showLoader();
    try {
        const response = await fetch('/api/medications');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        hideLoader();
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return [];
    }
}

// Get medication by ID
async function fetchMedicationById(id) {
    showLoader();
    try {
        const response = await fetch(`/api/medications/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        hideLoader();
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return null;
    }
}

// Create a new medication
async function createMedication(medicationData) {
    showLoader();
    try {
        const response = await fetch('/api/medications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(medicationData),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        hideLoader();
        showAlert('Medication created successfully!', 'success');
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return null;
    }
}

// Update an existing medication
async function updateMedication(id, medicationData) {
    showLoader();
    try {
        const response = await fetch(`/api/medications/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(medicationData),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        hideLoader();
        showAlert('Medication updated successfully!', 'success');
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return null;
    }
}

// Delete a medication
async function deleteMedication(id) {
    if (!confirm('Are you sure you want to delete this medication?')) {
        return false;
    }
    
    showLoader();
    try {
        const response = await fetch(`/api/medications/${id}`, {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        hideLoader();
        showAlert('Medication deleted successfully!', 'success');
        return true;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return false;
    }
}

// Similar functions for Health Metrics
async function fetchHealthMetrics(filters = {}) {
    showLoader();
    
    // Build query string from filters
    const queryParams = new URLSearchParams();
    if (filters.metric_type) queryParams.append('metric_type', filters.metric_type);
    if (filters.from_date) queryParams.append('from_date', filters.from_date);
    if (filters.to_date) queryParams.append('to_date', filters.to_date);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    try {
        const response = await fetch(`/api/health-metrics${queryString}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        hideLoader();
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return [];
    }
}

// Similar functions for Appointments
async function fetchAppointments(filters = {}) {
    showLoader();
    
    // Build query string from filters
    const queryParams = new URLSearchParams();
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.from_date) queryParams.append('from_date', filters.from_date);
    if (filters.to_date) queryParams.append('to_date', filters.to_date);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    try {
        const response = await fetch(`/api/appointments${queryString}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        hideLoader();
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return [];
    }
}

// Similar functions for Reminders
async function fetchReminders(filters = {}) {
    showLoader();
    
    // Build query string from filters
    const queryParams = new URLSearchParams();
    if (filters.reminder_type) queryParams.append('reminder_type', filters.reminder_type);
    if (filters.is_active !== undefined) queryParams.append('is_active', filters.is_active);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    
    try {
        const response = await fetch(`/api/reminders${queryString}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        hideLoader();
        return data;
    } catch (error) {
        hideLoader();
        handleFetchError(error);
        return [];
    }
}

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Health Management App Initialized');
    
    // Initialize any bootstrap components
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});