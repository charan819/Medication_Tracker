#!/usr/bin/env python3
"""
Local development startup script for Health Management System.
This script handles environment setup and database initialization.
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def check_docker():
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✓ Docker is available:", result.stdout.strip())
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Docker is not available. Please install Docker to continue.")
        return False

def check_database():
    """Check if PostgreSQL database is running."""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=health-tracker-db', '--format', 'table {{.Names}}\t{{.Status}}'], 
                              capture_output=True, text=True, check=True)
        if 'health-tracker-db' in result.stdout and 'Up' in result.stdout:
            print("✓ PostgreSQL database is running")
            return True
        else:
            print("✗ PostgreSQL database is not running")
            return False
    except subprocess.CalledProcessError:
        print("✗ Error checking database status")
        return False

def start_database():
    """Start PostgreSQL database using Docker Compose."""
    print("Starting PostgreSQL database...")
    try:
        if os.path.exists('docker-compose.yml'):
            result = subprocess.run(['docker-compose', 'up', '-d'], 
                                  capture_output=True, text=True, check=True)
            print("✓ Database started with Docker Compose")
        else:
            # Fallback to direct docker command
            docker_cmd = [
                'docker', 'run', '-d', '--name', 'health-tracker-db',
                '-e', 'POSTGRES_DB=health_tracker',
                '-e', 'POSTGRES_USER=health_user', 
                '-e', 'POSTGRES_PASSWORD=health_password',
                '-p', '5432:5432',
                'postgres:15'
            ]
            result = subprocess.run(docker_cmd, capture_output=True, text=True, check=True)
            print("✓ Database started with Docker")
        
        # Wait for database to be ready
        print("Waiting for database to be ready...")
        time.sleep(5)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start database: {e.stderr}")
        return False

def check_env_file():
    """Check if .env file exists and create from example if not."""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file from .env.example")
        else:
            print("✗ No .env file found and no .env.example to copy from")
            return False
    else:
        print("✓ Environment file found")
    return True

def start_application():
    """Start the Flask application."""
    print("Starting Health Management System...")
    try:
        # Load environment variables
        load_dotenv()
        
        # Start with gunicorn for better production-like experience
        subprocess.run([
            'gunicorn', 
            '--bind', '0.0.0.0:5000',
            '--reload',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'main:app'
        ])
    except KeyboardInterrupt:
        print("\n✓ Application stopped by user")
    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        # Fallback to python
        print("Trying fallback startup method...")
        subprocess.run([sys.executable, 'main.py'])

def main():
    """Main startup sequence."""
    print("🏥 Health Management System - Local Development Setup")
    print("=" * 55)
    
    # Check prerequisites
    if not check_docker():
        sys.exit(1)
    
    # Check environment file
    if not check_env_file():
        sys.exit(1)
    
    # Check/start database
    if not check_database():
        if not start_database():
            sys.exit(1)
        
        # Verify database started
        time.sleep(2)
        if not check_database():
            print("✗ Database failed to start properly")
            sys.exit(1)
    
    print("\n🚀 All prerequisites met! Starting application...")
    print("📝 Application will be available at: http://localhost:5000")
    print("🔧 API documentation at: http://localhost:5000/api/docs")
    print("⏹️  Press Ctrl+C to stop\n")
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()