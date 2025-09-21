# Contributing to Employee Analytics Project

We welcome contributions to the Employee Analytics Project! This document provides guidelines for contributing to the project.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Submitting Changes](#submitting-changes)
7. [Reporting Issues](#reporting-issues)

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (or NeonDB cloud database)
- Git
- Virtual environment tool (venv, virtualenv, etc.)

### Setting Up Your Development Environment

1. **Fork the Repository**
   - Fork the repository on GitHub
   - Clone your fork locally:
     ```bash
     git clone https://github.com/your-username/employee-analytics.git
     cd employee-analytics
     ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scriptsctivate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project root
   - Copy the template from `.env.example` (if available)
   - Fill in your database credentials and other settings

5. **Set Up Database**
   ```bash
   # Create database migrations
   python employee-analytics/manage.py makemigrations

   # Apply migrations
   python employee-analytics/manage.py migrate

   # Create a superuser (optional)
   python employee-analytics/manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```bash
   python employee-analytics/manage.py runserver
   ```

---

## Development Workflow

### Creating a Feature Branch

1. Create a feature branch from `main` or `develop`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request to the main repository

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

Examples:
```
feat: Add employee performance tracking
fix: Resolve database connection error
docs: Update API documentation
refactor: Optimize query performance
test: Add unit tests for employee model
```

---

## Code Style

### Python Code Style
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation (no tabs)
- Limit lines to 79 characters
- Use meaningful variable and function names

### Django Best Practices
- Use Django's built-in features where possible
- Follow Django's project structure conventions
- Use Django's ORM instead of raw SQL queries
- Implement proper error handling

### Example Code Style

```python
# Good example
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    """Model representing an employee."""

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hire_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    def full_name(self):
        """Return the employee's full name."""
        return f"{self.first_name} {self.last_name}"
```

---

## Testing

### Running Tests
```bash
# Run all tests
python employee-analytics/manage.py test

# Run tests for a specific app
python employee-analytics/manage.py test employees

# Run tests with verbose output
python employee-analytics/manage.py test --verbosity=2

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests
- Follow Django's testing framework
- Write unit tests for models, views, and utility functions
- Write integration tests for API endpoints
- Aim for high test coverage (80% or higher)

### Example Test Case

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Employee
from ..serializers import EmployeeSerializer


class EmployeeModelTests(TestCase):
    """Test cases for the Employee model."""

    def setUp(self):
        """Set up test data."""
        self.employee = Employee.objects.create(
            employee_id="EMP001",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )

    def test_employee_creation(self):
        """Test that an employee can be created."""
        self.assertEqual(self.employee.employee_id, "EMP001")
        self.assertEqual(self.employee.first_name, "John")
        self.assertEqual(self.employee.last_name, "Doe")
        self.assertEqual(self.employee.email, "john.doe@example.com")

    def test_employee_str_method(self):
        """Test the string representation of an employee."""
        self.assertEqual(str(self.employee), "John Doe (EMP001)")


class EmployeeAPITests(TestCase):
    """Test cases for the Employee API."""

    def setUp(self):
        """Set up test data."""
        self.employee = Employee.objects.create(
            employee_id="EMP001",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        self.url = reverse('employee-list')

    def test_get_employee_list(self):
        """Test retrieving a list of employees."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_employee_detail(self):
        """Test retrieving a single employee."""
        url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_id'], "EMP001")
```

---

## Documentation

### Code Documentation
- Use docstrings for all modules, classes, functions, and methods
- Follow Google or NumPy style for docstrings
- Include examples where helpful

### API Documentation
- Update API documentation when adding new endpoints
- Use OpenAPI/Swagger specifications
- Include examples of request and response bodies

### User Documentation
- Update README.md with any new setup requirements
- Create or update guides for complex features
- Include screenshots where helpful

---

## Submitting Changes

### Pull Request Guidelines

1. **Create a Pull Request**
   - Give your PR a clear and descriptive title
   - Link to any related issues
   - Provide a detailed description of your changes

2. **PR Checklist**
   - All tests pass
   - Code follows the project's style guidelines
   - Documentation is updated if necessary
   - The PR description clearly explains the changes

3. **Addressing Feedback**
   - Respond to reviewer comments
   - Make necessary changes
   - Add new commits to the same branch
   - Push updated changes to your branch

4. **Final Review**
   - Ensure all issues are resolved
   - Wait for final approval
   - Your PR will be merged by a maintainer

---

## Reporting Issues

### Bug Reports
When reporting a bug, please include:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Environment information (OS, Python version, etc.)
- Error messages or stack traces (if applicable)

### Feature Requests
When requesting a feature, please include:
- A clear and descriptive title
- A detailed description of the requested feature
- Use cases for the feature
- Any mockups or examples if applicable

### Security Issues
For security vulnerabilities, please:
- Do not report them publicly
- Email the development team directly
- Provide as much detail as possible without exposing the vulnerability

---

## Code of Conduct

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions with the project community.

---

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [License](LICENSE).
