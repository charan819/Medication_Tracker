# Health Management System

## Overview

This is a Flask-based health management web application that helps users track medications, monitor health metrics, manage appointments, and set reminders. The system provides both a web interface and RESTful API endpoints for comprehensive health data management.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 (Replit dark theme)
- **JavaScript**: Vanilla JavaScript with fetch API for AJAX requests
- **Styling**: Bootstrap 5 with custom CSS, Font Awesome icons
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Backend Architecture
- **Framework**: Flask with Flask-RESTful for API endpoints
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Data Validation**: Marshmallow schemas for serialization/deserialization
- **Database Migrations**: Flask-Migrate (Alembic)
- **CORS**: Flask-CORS for cross-origin requests

### API Design
- RESTful API with resource-based endpoints
- JSON request/response format
- Swagger/OpenAPI documentation ready
- Filtering and pagination support for list endpoints

## Key Components

### Models (Database Schema)
1. **Medication**: Stores medication information with dosage, frequency, and intake times
2. **MedicationLog**: Tracks when medications were taken, skipped, or missed  
3. **HealthMetric**: Records various health measurements (blood pressure, glucose, weight, etc.)
4. **Appointment**: Manages healthcare appointments with providers
5. **Reminder**: Handles medication, appointment, and health check reminders

### Services
1. **NotificationService**: Manages push notifications and email alerts
2. **EmailService**: SendGrid integration for email notifications
3. **ChatbotService**: ChatGPT-4o integration for AI health assistance

### API Resources
- **MedicationResource**: CRUD operations for individual medications
- **MedicationListResource**: List and create medications with filtering
- **HealthMetricResource**: Manage individual health metric records
- **AppointmentResource**: Handle appointment scheduling and updates
- **ReminderResource**: Manage reminder notifications
- **NotificationResource**: Handle push notifications and email alerts
- **ChatbotResource**: ChatGPT-powered health assistant endpoints

### Data Management
- **JSON Repository Pattern**: Fallback data storage using JSON files
- **Database Seeding**: Automated population of dummy data for development
- **Data Validation**: Comprehensive input validation using Marshmallow schemas

## Data Flow

1. **Web Interface**: Users interact through HTML templates rendered by Flask
2. **API Layer**: JavaScript makes AJAX calls to Flask-RESTful endpoints
3. **Validation**: Marshmallow schemas validate incoming data
4. **Business Logic**: Flask resources handle CRUD operations
5. **Data Persistence**: SQLAlchemy manages database interactions
6. **Response**: JSON responses sent back to frontend for display

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework and application factory
- **SQLAlchemy**: Database ORM and query builder
- **Marshmallow**: Data serialization and validation
- **Flask-Migrate**: Database schema migrations

### Additional Libraries
- **Flask-RESTful**: RESTful API development
- **Flask-CORS**: Cross-origin resource sharing
- **Werkzeug**: WSGI utilities and middleware
- **Bootstrap 5**: Frontend CSS framework (CDN)
- **Font Awesome**: Icon library (CDN)

### Database Support
- **SQLite**: Default development database
- **PostgreSQL**: Production database support via DATABASE_URL environment variable

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database with debug mode enabled
- **Production**: PostgreSQL database with security hardening
- **Testing**: In-memory SQLite database for unit tests

### Configuration Management
- Environment-based configuration using config.py
- Sensitive data managed through environment variables
- Separate configurations for development, production, and testing

### Database Strategy
- **Migration System**: Alembic-based migrations for schema changes  
- **Connection Pooling**: Configured for production environments
- **Fallback Data**: JSON-based repository for development without database

### Deployment Considerations
- WSGI application with ProxyFix middleware for reverse proxy compatibility
- CORS configured for cross-origin requests
- Session security configured for production environments

## Changelog
- June 30, 2025. Initial setup
- June 30, 2025. Fixed circular import issues by creating separate database.py module
- June 30, 2025. Added environment variable support with .env files
- June 30, 2025. Created comprehensive README with local development setup instructions
- June 30, 2025. Added Docker Compose configuration for PostgreSQL database
- June 30, 2025. Successfully resolved application startup issues for local development
- July 5, 2025. Implemented comprehensive push notification system with browser notifications
- July 5, 2025. Added email notification service with SendGrid integration
- July 5, 2025. Created ChatGPT-4o powered health assistant with conversational AI capabilities
- July 5, 2025. Added notification management API and user interface

## User Preferences

Preferred communication style: Simple, everyday language.