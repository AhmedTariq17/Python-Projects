#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Import the os module to interact with the operating system
import os

# Import the sys module to work with command-line arguments
import sys

# Define the main function to execute administrative tasks
def main():
    """Run administrative tasks."""
    # Set the default settings module for the Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
    
    try:
        # Import the execute_from_command_line function to handle command-line arguments
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an ImportError with a descriptive message if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command-line utility with the provided arguments
    execute_from_command_line(sys.argv)

# Check if this script is being run as the main program
if __name__ == '__main__':
    main()
