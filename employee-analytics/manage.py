#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

This script is the entry point for Django's management commands.
It allows running various administrative tasks like:
- Running the development server
- Making database migrations
- Creating superusers
- Collecting static files
- And many more Django management commands
"""
import os  # Operating system interface
import sys  # System-specific parameters and functions


def main():
    """Run administrative tasks.
    
    This function is the main entry point for Django management commands.
    It sets up the Django environment and executes the specified command.
    """
    # Set the default Django settings module
    # This tells Django which settings file to use for configuration
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_analytics.settings')
    
    try:
        # Import Django's command line execution function
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error message if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command specified in the command line arguments
    execute_from_command_line(sys.argv)


# This block ensures that the main() function is called only when the script is executed directly
if __name__ == '__main__':
    main()
