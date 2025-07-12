from app import app  # noqa: F401
import os
from seed_database import seed_all

"""
Health Management API

This application provides endpoints for managing health-related data, including:
- Medications and medication logs
- Health metrics (blood pressure, glucose, weight, etc.)
- Appointments with healthcare providers
- Reminders for medications, appointments, and health checks

The application uses PostgreSQL database for data storage.
"""

# These imports are here to avoid circular imports
from resources.medication import MedicationResource, MedicationListResource, MedicationLogResource, MedicationStatusResource
from resources.health_metrics import HealthMetricResource, HealthMetricListResource
from resources.appointment import AppointmentResource, AppointmentListResource, AppointmentStatusResource
from resources.reminder import ReminderResource, ReminderListResource

# Skip seeding during authentication refactor
# with app.app_context():
#     seed_all()

if __name__ == "__main__":
    # This code only runs when the script is executed directly, not when imported
    # The server should be started with gunicorn for production, but this is useful for development
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)