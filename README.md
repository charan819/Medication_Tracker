# Health Management System

A comprehensive web application for managing personal health data including medications, health metrics, appointments, and reminders. Built with Flask and PostgreSQL.

## Features

- **Medication Management**: Track medications, dosages, schedules, and intake logs
- **Health Metrics**: Monitor vital signs like blood pressure, glucose, weight, and more
- **Appointment Scheduling**: Manage healthcare appointments with providers
- **Reminder System**: Set up notifications for medications and appointments
- **Push Notifications**: Real-time browser notifications for due reminders
- **Email Alerts**: Email notifications via SendGrid integration
- **AI Health Assistant**: ChatGPT-powered chatbot for health guidance and wellness tips
- **RESTful API**: Complete API endpoints for all health data management
- **Web Interface**: User-friendly web UI with responsive Bootstrap design

## Architecture

- **Backend**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Frontend**: Bootstrap 5 with vanilla JavaScript
- **API**: RESTful endpoints with JSON responses
- **Validation**: Marshmallow schemas for data validation

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for PostgreSQL)
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd health-management-system
```

### 2. Set Up Docker PostgreSQL Database

**Option A: Using Docker Compose (Recommended)**

```bash
# Start the database with persistent data
docker-compose up -d

# Verify the database is running
docker-compose ps
```

**Option B: Using Docker directly**

```bash
docker run -d --name health-tracker-db \
  -e POSTGRES_DB=health_tracker \
  -e POSTGRES_USER=health_user \
  -e POSTGRES_PASSWORD=health_password \
  -p 5432:5432 \
  postgres:15
```

Verify the database is running:
```bash
docker ps
```

### 3. Install Python Dependencies

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your settings:

```bash
# Health Management Application Environment Variables
SESSION_SECRET=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration - Dockerized PostgreSQL
DATABASE_URL=postgresql://health_user:health_password@localhost:5432/health_tracker

# CORS Configuration
CORS_ORIGINS=*

# Logging Configuration
LOG_LEVEL=DEBUG
```

### 5. Start the Application

**Option A: Automated Setup (Recommended)**

Use the provided startup script that handles database setup and application startup:

```bash
python start_local.py
```

This script will:
- Check Docker availability
- Start PostgreSQL database if needed
- Create environment file from template
- Start the Flask application with hot reload

**Option B: Manual Setup**

Initialize the database and start manually:

```bash
# Start the application (will auto-create tables and seed data)
python main.py
```

Or run with Gunicorn (production-like):
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### 6. Access the Application

- **Web Interface**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/docs
- **API Base URL**: http://localhost:5000/api

## API Endpoints

### Medications
- `GET /api/medications` - List all medications
- `POST /api/medications` - Create new medication
- `GET /api/medications/{id}` - Get specific medication
- `PUT /api/medications/{id}` - Update medication
- `DELETE /api/medications/{id}` - Delete medication
- `POST /api/medications/{id}/logs` - Add medication log
- `PUT /api/medications/{id}/status` - Update medication status

### Health Metrics
- `GET /api/health-metrics` - List all health metrics
- `POST /api/health-metrics` - Create new health metric
- `GET /api/health-metrics/{id}` - Get specific health metric
- `PUT /api/health-metrics/{id}` - Update health metric
- `DELETE /api/health-metrics/{id}` - Delete health metric

### Appointments
- `GET /api/appointments` - List all appointments
- `POST /api/appointments` - Create new appointment
- `GET /api/appointments/{id}` - Get specific appointment
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Delete appointment
- `PUT /api/appointments/{id}/status` - Update appointment status

### Reminders
- `GET /api/reminders` - List all reminders
- `POST /api/reminders` - Create new reminder
- `GET /api/reminders/{id}` - Get specific reminder
- `PUT /api/reminders/{id}` - Update reminder
- `DELETE /api/reminders/{id}` - Delete reminder

### Notifications
- `GET /api/notifications` - Get pending notifications
- `PUT /api/notifications/{id}` - Mark notification as read
- `POST /api/notifications/test` - Send test notification
- `GET /api/notifications/settings` - Get notification service status

### ChatGPT Health Assistant
- `POST /api/chatbot` - Send message to health assistant
- `GET /api/chatbot/tips/{category}` - Get health tips for specific category
- `GET /api/chatbot/status` - Check chatbot service status

## Database Management

### Resetting the Database

To clear all data and reseed:

```bash
python seed_database.py
```

### Database Migrations

For schema changes, use Flask-Migrate:

```bash
# Initialize migrations (first time only)
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## Production Deployment

### Environment Variables for Production

Update your `.env` file for production:

```bash
# Production Configuration
SESSION_SECRET=your-production-secret-key
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration for EC2/Production
DATABASE_URL=postgresql://health_user:health_password@your-production-host:5432/health_tracker

# Security Settings
CORS_ORIGINS=https://yourdomain.com

# Logging
LOG_LEVEL=INFO
```

### Deployment Options

1. **Replit Deployment**: Use Replit's built-in deployment features
2. **AWS EC2**: Deploy to EC2 instance with PostgreSQL RDS
3. **Docker**: Use Docker containers for both app and database
4. **Heroku**: Deploy with Heroku PostgreSQL add-on

### Security Considerations

- Change the `SESSION_SECRET` to a strong, unique value
- Use HTTPS in production
- Restrict CORS origins to your domain
- Set up proper database user permissions
- Use environment variables for all sensitive data

## Development

### Project Structure

```
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── database.py         # Database initialization
├── models.py           # SQLAlchemy models
├── schemas.py          # Marshmallow schemas
├── config.py           # Configuration settings
├── resources/          # API resource classes
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, and assets
├── utils/              # Utility functions
├── migrations/         # Database migrations
└── data/               # Sample data files
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL container is running
   - Check DATABASE_URL in .env file
   - Verify database credentials

2. **Circular Import Error**
   - The application uses proper import structure to avoid circular imports
   - If issues persist, check the database.py module initialization

3. **Port Already in Use**
   - Change the port in the run command: `--bind 0.0.0.0:8000`
   - Or kill the process using the port

4. **Missing Dependencies**
   - Run `pip install -r requirements.txt`
   - Ensure you're in the correct virtual environment

### Database Management Commands

```bash
# Stop and remove existing database container
docker stop health-tracker-db
docker rm health-tracker-db

# Start fresh database
docker run -d --name health-tracker-db \
  -e POSTGRES_DB=health_tracker \
  -e POSTGRES_USER=health_user \
  -e POSTGRES_PASSWORD=health_password \
  -p 5432:5432 postgres:15

# Connect to database directly
docker exec -it health-tracker-db psql -U health_user -d health_tracker
```

## Notification System

The Health Management System includes a comprehensive notification system with both browser push notifications and email alerts.

### Features

- **Browser Push Notifications**: Real-time notifications in your browser
- **Email Notifications**: SendGrid-powered email alerts
- **Automatic Scheduling**: Reminders are automatically scheduled when created
- **Multiple Notification Types**: Medication, appointment, and health check reminders
- **Recurring Reminders**: Support for daily, weekly, and monthly repeats

### Setup Email Notifications

To enable email notifications, configure SendGrid in your environment:

```bash
# Add to your .env file
SENDGRID_API_KEY=your-sendgrid-api-key-here
FROM_EMAIL=noreply@yourdomain.com
USER_EMAIL=your-email@example.com
```

### Getting SendGrid API Key

1. Sign up for a free SendGrid account at https://sendgrid.com
2. Navigate to Settings > API Keys
3. Create a new API key with "Mail Send" permissions
4. Add the API key to your environment variables

### Browser Notifications

Browser notifications work automatically and require user permission:

1. Visit the **Notifications** page in the application
2. Click "Enable Push Notifications" when prompted
3. Allow notifications in your browser

### Testing Notifications

Use the notification settings page to:

- Test push notifications
- Test email delivery
- View notification status
- Create quick reminders
- Manage notification preferences

### Notification API

The system provides REST API endpoints for notification management:

```bash
# Get pending notifications
curl http://localhost:5000/api/notifications

# Send test notification
curl -X POST http://localhost:5000/api/notifications/test

# Get notification service status
curl http://localhost:5000/api/notifications/settings
```

## ChatGPT Health Assistant

The Health Management System includes an AI-powered health assistant using ChatGPT-4o to provide personalized health guidance and wellness support.

### Features

- **Interactive Health Chat**: Ask questions about medications, health metrics, and wellness
- **Health Tips by Category**: Get curated advice for general health, medication, exercise, nutrition, sleep, and stress management
- **Conversation Memory**: Maintains context across the conversation for more relevant responses
- **Health Context Awareness**: Understands your health tracking data and provides relevant guidance
- **Professional Guidelines**: Always recommends consulting healthcare professionals for medical advice

### Setup ChatGPT Integration

To enable the AI health assistant, configure OpenAI in your environment:

```bash
# Add to your .env file
OPENAI_API_KEY=your-openai-api-key-here
```

### Getting OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Sign in or create an OpenAI account
3. Click "Create new secret key" 
4. Copy the key (starts with "sk-")
5. Add the key to your environment variables
6. Ensure you have billing set up for API usage

### Using the Health Assistant

#### Web Interface

1. Click "Health Assistant" in the navigation menu
2. Use quick health tip buttons for instant advice
3. Type questions in the chat interface
4. Get personalized responses powered by ChatGPT-4o

#### API Usage

```bash
# Send a message to the health assistant
curl -X POST http://localhost:5000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "What are some tips for taking medications consistently?"}'

# Get health tips for specific categories
curl http://localhost:5000/api/chatbot/tips/medication
curl http://localhost:5000/api/chatbot/tips/exercise
curl http://localhost:5000/api/chatbot/tips/nutrition

# Check chatbot service status
curl http://localhost:5000/api/chatbot/status
```

### Health Tip Categories

- **General**: Overall wellness and health maintenance
- **Medication**: Medication management and adherence tips
- **Exercise**: Physical activity and fitness guidance
- **Nutrition**: Healthy eating and dietary advice
- **Sleep**: Sleep hygiene and rest quality
- **Stress**: Stress management and mental wellness

### Important Notes

- The AI assistant provides general health information only
- Always consult healthcare professionals for medical advice
- Responses are generated by ChatGPT-4o with health-specific context
- API usage requires an active OpenAI account with billing configured

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request
