# Employee Analytics Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [API Documentation](#api-documentation)
8. [Admin Interface](#admin-interface)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)

---

## Project Overview

The Employee Analytics Project is a comprehensive Django-based system designed to manage employee data, track attendance, evaluate performance, and provide analytical insights. Built with Django and Django REST Framework, this project offers both a web admin interface and RESTful API endpoints for seamless data management and integration.

### Key Features
- Employee management with departments and positions
- Attendance tracking with comprehensive records
- Performance evaluation system with reviews and goals
- Analytics dashboard for data visualization
- RESTful API with Swagger documentation
- Admin interface improvements for better data handling

### Technology Stack
- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: PostgreSQL (with NeonDB support)
- **Documentation**: drf-yasg (Swagger)
- **Frontend**: Django Admin Interface
- **Testing**: Django Test Framework

---

## Project Structure

```
assigbment/
├── README.md                    # Project documentation
├── RUN_SERVER.md               # Detailed server setup guide
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (excluded from git)
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker services configuration
├── cleanup.bat                # Windows cleanup script
└── employee-analytics/        # Main Django project directory
    ├── manage.py              # Django management script
    ├── employee_analytics/     # Project settings and configuration
    │   ├── __init__.py
    │   ├── settings.py        # Django settings
    │   ├── urls.py            # Main URL configuration
    │   ├── asgi.py            # ASGI configuration
    │   └── wsgi.py            # WSGI configuration
    ├── apps/                  # Django applications
    │   ├── __init__.py
    │   ├── analytics/         # Analytics application
    │   ├── attendance/        # Attendance tracking application
    │   ├── employees/         # Employee management application
    │   └── performance/       # Performance evaluation application
    ├── requirements/          # Project requirements
    │   └── base.txt          # Base requirements
    ├── static/               # Static files (CSS, JS, images)
    │   └── js/
    ├── templates/            # HTML templates
    │   └── swagger/
    └── utils/               # Utility functions and scripts
        ├── __init__.py
        ├── data_generator.py  # Sample data generation
        ├── pagination.py      # Custom pagination
        ├── permissions.py     # Custom permissions
        └── sample_data.py     # Sample data creation
```

### File Naming Conventions

#### Python Files
- **Models**: `models.py` - Contains database models
- **Views**: `views.py` - Contains view logic
- **Serializers**: `serializers.py` - API serializers
- **Urls**: `urls.py` - URL patterns
- **Admin**: `admin.py` - Admin interface configuration
- **Tests**: `tests.py` - Test cases
- **Forms**: `forms.py` - Form definitions
- **Middleware**: `middleware.py` - Custom middleware
- **Mixins**: `mixins.py` - Reusable view components
- **Constants**: `constants.py` - Application constants
- **Exceptions**: `exceptions.py` - Custom exceptions

#### Documentation Files
- **README**: `README.md` - Project overview and setup instructions
- **API Documentation**: `API_DOCUMENTATION.md` - Detailed API reference
- **Setup Guide**: `SETUP.md` - Detailed setup instructions
- **Changelog**: `CHANGELOG.md` - Version history and updates
- **Contributing**: `CONTRIBUTING.md` - Guidelines for contributors

#### Environment and Configuration Files
- **Environment**: `.env` - Environment variables
- **Docker**: `Dockerfile` - Docker configuration
- **Docker Compose**: `docker-compose.yml` - Docker services configuration
- **Requirements**: `requirements.txt` - Python dependencies

---

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (or cloud-based like NeonDB)
- Virtual environment tool (venv, virtualenv, etc.)
- Git (for repository cloning)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd assigbment
```

#### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
# Install project dependencies
pip install -r requirements.txt
```

#### 4. Environment Configuration
Create a `.env` file in the project root directory. See [Environment Configuration](#environment-configuration) section for details.

#### 5. Database Setup
Configure your database settings and run migrations. See [Database Setup](#database-setup) section for details.

#### 6. Create Superuser (Optional)
```bash
python employee-analytics/manage.py createsuperuser
```

#### 7. Generate Sample Data (Optional)
```bash
python employee-analytics/manage.py shell -c "from utils.sample_data import create_sample_data; create_sample_data()"
```

---

## Environment Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings - PostgreSQL/NeonDB
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
DB_OPTIONS=sslmode=require

# API settings
API_RATE_LIMIT=100/day
API_BURST_RATE=10/hour
```

### Environment File Naming Conventions
- `.env` - Default environment file
- `.env.local` - Local overrides
- `.env.development` - Development environment
- `.env.staging` - Staging environment
- `.env.production` - Production environment
- `.env.test` - Testing environment

### Environment Security
- Never commit environment files to version control
- Use strong, unique secret keys
- Rotate database credentials regularly
- Use environment-specific configurations

---

## Database Setup

### PostgreSQL Configuration
1. Install PostgreSQL if not already installed
2. Create a new database for the project
3. Update the database settings in `employee-analytics/employee_analytics/settings.py` or in the `.env` file

Example configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host',
        'PORT': 'your_db_port',
    }
}
```

### NeonDB Configuration (Cloud-based PostgreSQL)
1. Create a NeonDB account at https://neon.tech/
2. Create a new project and database
3. Get database connection string from NeonDB dashboard
4. Update the `.env` file with the connection details

### Database Migrations
```bash
# Create migrations
python employee-analytics/manage.py makemigrations

# Apply migrations
python employee-analytics/manage.py migrate
```

### Sample Data Generation
To populate the database with sample data for testing:
```bash
python employee-analytics/manage.py shell -c "from utils.sample_data import create_sample_data; create_sample_data()"
```

---

## Running the Application

### Development Server
```bash
# Start the development server
python employee-analytics/manage.py runserver
```

Access the application at:
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/swagger/

### Production Deployment
For production deployment, refer to the detailed deployment guide in `RUN_SERVER.md`.

### Docker Deployment
```bash
# Build the Docker image
docker build -t employee-analytics .

# Run the container
docker run -p 8000:8000 employee-analytics
```

Or using Docker Compose:
```bash
docker-compose up --build
```

---

## API Documentation

The project includes Swagger UI for interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

### API Endpoints

#### Employee Management
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create a new employee
- `GET /api/employees/{id}/` - Retrieve an employee
- `PUT /api/employees/{id}/` - Update an employee
- `DELETE /api/employees/{id}/` - Delete an employee

#### Attendance Tracking
- `GET /api/attendances/` - List all attendance records
- `POST /api/attendances/` - Create a new attendance record
- `GET /api/attendances/?employee_id=EMP12345` - Filter by employee

#### Performance Evaluation
- `GET /api/performances/` - List all performance records
- `POST /api/performances/` - Create a new performance record
- `GET /api/performances/?employee_id=EMP12345` - Filter by employee

#### Analytics
- `GET /api/summary/attendance/` - Attendance summary
- `GET /api/summary/performance/` - Performance summary
- `GET /api/departments/summary/` - Department summary

---

## Admin Interface

The Django admin interface provides a convenient way to manage application data:

### Accessing the Admin Interface
1. Create a superuser account:
   ```bash
   python employee-analytics/manage.py createsuperuser
   ```
2. Access the admin interface at: http://127.0.0.1:8000/admin/

### Admin Interface Improvements
- Employee admin displays department and position titles properly
- Performance and Review admin display employee names clearly
- Graceful handling of missing or null related objects
- Custom admin views for better data visualization

---

## Testing

### Running Tests
```bash
# Run all tests
python employee-analytics/manage.py test

# Run tests for specific app
python employee-analytics/manage.py test employees

# Run tests with verbose output
python employee-analytics/manage.py test --verbosity=2
```

### Testing Approach

#### Critical-path Testing
- Verify key admin pages (Employee, Attendance, Performance, Reviews)
- Test basic CRUD operations for all API endpoints
- Check authentication and authorization

#### Thorough Testing
- Exercise all API endpoints with various inputs
- Test edge cases and error handling
- Navigate all admin pages and test all forms and filters
- Validate data integrity and constraints

### Test Coverage
- Aim for high test coverage of critical functionality
- Include unit tests for models and views
- Include integration tests for API endpoints

---

## Troubleshooting

### Common Issues

#### Database Connection Errors
1. Verify database credentials in `.env` file
2. Check database service is running
3. Ensure proper network connectivity
4. For NeonDB, verify SSL settings

#### Migration Issues
1. Delete all migration files in app directories except `__init__.py`
2. Run `python employee-analytics/manage.py makemigrations`
3. Run `python employee-analytics/manage.py migrate --fake-initial`

#### Server Won't Start
1. Check if port 8000 is already in use
2. Verify all dependencies are installed
3. Check Django settings for syntax errors
4. Ensure proper virtual environment activation

### Debug Mode
Enable Django's debug mode for detailed error information:
```python
# In settings.py
DEBUG = True
```

### Logging
Configure logging for better debugging:
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Update documentation if needed
7. Submit a pull request

### Code Style Guidelines
- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all public modules, functions, classes, and methods
- Keep functions and classes focused and single-purpose
- Write clean, readable, and maintainable code

### Commit Message Conventions
- Use clear and descriptive commit messages
- Follow the format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Example: `feat(employee): add employee performance evaluation endpoint`

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Support

For further assistance or issues, please:
1. Check the troubleshooting section
2. Search existing issues in the repository
3. Create a new issue with detailed description
4. Contact the development team with specific questions

### Additional Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [NeonDB Documentation](https://neon.tech/docs)
