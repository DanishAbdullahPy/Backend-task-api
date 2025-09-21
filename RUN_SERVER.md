# Server Setup and Running Guide

This guide will help you set up and run the Employee Data Generation & Visualization System with NeonDB PostgreSQL.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL client libraries (psycopg2)
- NeonDB PostgreSQL account

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the project root with the following content:

```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings - NeonDB PostgreSQL
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=npg_8bVDOLRlhIf1
DB_HOST=ep-rapid-bird-adoq6axv-pooler.c-2.us-east-1.aws.neon.tech
DB_PORT=5432
DB_OPTIONS=sslmode=require

# API settings
API_RATE_LIMIT=100/day
API_BURST_RATE=10/hour
```

### 2. Install Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Database Migrations

```bash
# Apply database migrations
python manage.py migrate
```

### 4. Create a Superuser (Optional)

```bash
# Create a superuser for admin access
python manage.py createsuperuser
```

### 5. Generate Sample Data

```bash
# Generate sample employee data
python manage.py generate_sample_data --count 5
```

### 6. Start the Development Server

```bash
# Start the development server
python manage.py runserver
```

## Access Points

Once the server is running, you can access the following:

- **API Documentation**: http://127.0.0.1:8000/swagger/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Health Check**: http://127.0.0.1:8000/health/

## Testing with Postman

### 1. Authentication

First, you need to get an authentication token:

- **Endpoint**: `POST http://127.0.0.1:8000/api/auth/login/`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### 2. Employee Endpoints

- **Get all employees**: `GET http://127.0.0.1:8000/api/employees/`
- **Get employee by ID**: `GET http://127.0.0.1:8000/api/employees/{id}/`
- **Create new employee**: `POST http://127.0.0.1:8000/api/employees/`
- **Update employee**: `PUT http://127.0.0.1:8000/api/employees/{id}/`
- **Delete employee**: `DELETE http://127.0.0.1:8000/api/employees/{id}/`

### 3. Attendance Endpoints

- **Get all attendance records**: `GET http://127.0.0.1:8000/api/attendances/`
- **Get attendance by employee ID**: `GET http://127.0.0.1:8000/api/attendances/?employee_id=EMP12345`
- **Create attendance record**: `POST http://127.0.0.1:8000/api/attendances/`

### 4. Performance Endpoints

- **Get all performance records**: `GET http://127.0.0.1:8000/api/performances/`
- **Get performance by employee ID**: `GET http://127.0.0.1:8000/api/performances/?employee_id=EMP12345`
- **Create performance record**: `POST http://127.0.0.1:8000/api/performances/`

### 5. Department Endpoints

- **Get all departments**: `GET http://127.0.0.1:8000/api/departments/`
- **Get department summary**: `GET http://127.0.0.1:8000/api/departments/summary/`

### 6. Analytical Summary Endpoints

- **Get attendance summary**: `GET http://127.0.0.1:8000/api/summary/attendance/`
- **Get performance summary**: `GET http://127.0.0.1:8000/api/summary/performance/`

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Verify your NeonDB credentials in the `.env` file
2. Check your internet connection (NeonDB is cloud-based)
3. Ensure the SSL mode is set to 'require'

### Migration Issues

If you encounter migration issues:

1. Delete all migration files in `employee_data/migrations/` except `__init__.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate --fake-initial`

### Server Won't Start

If the server won't start:

1. Check if port 8000 is already in use
2. Verify all dependencies are installed correctly
3. Check the Django settings for any syntax errors
