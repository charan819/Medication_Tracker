import os
import logging
from flask import Flask, render_template, redirect, url_for
from flask_restful import Api
from flask_login import LoginManager, login_required
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from database import db, ma, migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=getattr(logging, log_level.upper()))

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "health-app-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure CORS to allow requests from any origin
CORS(app)

# Configure the database with fallback to SQLite
database_url = os.environ.get("DATABASE_URL")
if not database_url or 'neon.tech' in database_url:
    # Use SQLite for development if PostgreSQL is unavailable
    database_url = "sqlite:///health_management.db"
    logging.info("Using SQLite database for development")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extensions
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Initialize API
api = Api(app)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models
    import models  # noqa: F401

    # Create database tables - force recreation with new schema
    try:
        db.drop_all()  # Drop existing tables first
        db.create_all()  # Create with new schema including user_id columns
        logging.info("Database tables recreated successfully with new schema")
    except Exception as e:
        logging.error(f"Could not create database tables: {e}")
        raise
    
    # API Documentation
    @app.route('/api/docs')
    def api_docs():
        return "API Documentation - To be implemented"
        
    # Web UI Routes with authentication
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return render_template('index.html')
        else:
            return redirect(url_for('auth.login'))
        
    @app.route('/medications')
    @login_required
    def medications():
        return render_template('medications.html')
        
    @app.route('/medications/<int:medication_id>')
    @login_required
    def medication_detail(medication_id):
        return render_template('medication_detail.html', medication_id=medication_id)
        
    @app.route('/health-metrics')
    @login_required
    def health_metrics():
        return render_template('health_metrics.html')
        
    @app.route('/appointments')
    @login_required
    def appointments():
        return render_template('appointments.html')
        
    @app.route('/reminders')
    @login_required
    def reminders():
        return render_template('reminders.html')

    @app.route('/notifications')
    @login_required
    def notifications():
        return render_template('notifications.html')

    @app.route('/chatbot')
    @login_required
    def chatbot():
        return render_template('chatbot.html')

    # Register authentication blueprint
    from auth import auth_bp
    app.register_blueprint(auth_bp)

# These imports are below app.app_context to avoid circular imports
from resources.medication import MedicationResource, MedicationListResource, MedicationLogResource, MedicationStatusResource
from resources.health_metrics import HealthMetricResource, HealthMetricListResource
from resources.appointment import AppointmentResource, AppointmentListResource, AppointmentStatusResource
from resources.reminder import ReminderResource, ReminderListResource
from resources.notification import NotificationListResource, NotificationResource, NotificationTestResource, NotificationSettingsResource

# Register API endpoints
api.add_resource(MedicationListResource, '/api/medications')
api.add_resource(MedicationResource, '/api/medications/<int:medication_id>')
api.add_resource(MedicationStatusResource, '/api/medications/<int:medication_id>/status')
api.add_resource(MedicationLogResource, '/api/medications/<int:medication_id>/logs')

api.add_resource(HealthMetricListResource, '/api/health-metrics')
api.add_resource(HealthMetricResource, '/api/health-metrics/<int:metric_id>')

api.add_resource(AppointmentListResource, '/api/appointments')
api.add_resource(AppointmentResource, '/api/appointments/<int:appointment_id>')
api.add_resource(AppointmentStatusResource, '/api/appointments/<int:appointment_id>/status')

api.add_resource(ReminderListResource, '/api/reminders')
api.add_resource(ReminderResource, '/api/reminders/<int:reminder_id>')

api.add_resource(NotificationListResource, '/api/notifications')
api.add_resource(NotificationResource, '/api/notifications/<string:notification_id>')
api.add_resource(NotificationTestResource, '/api/notifications/test')
api.add_resource(NotificationSettingsResource, '/api/notifications/settings')

# Import and register chatbot resources
from resources.chatbot import ChatbotResource, ChatbotHealthTipsResource, ChatbotStatusResource
api.add_resource(ChatbotResource, '/api/chatbot')
api.add_resource(ChatbotHealthTipsResource, '/api/chatbot/tips', '/api/chatbot/tips/<string:category>')
api.add_resource(ChatbotStatusResource, '/api/chatbot/status')

# Initialize notification service
with app.app_context():
    try:
        from services.notification_service import notification_service
        notification_service.initialize_all_reminders()
        logging.info("Notification service initialized and reminders scheduled")
    except Exception as e:
        logging.error(f"Failed to initialize notification service: {e}")
