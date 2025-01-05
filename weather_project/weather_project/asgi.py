"""
ASGI config for weather_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# Import the os module to interact with the operating system
import os

# Import the get_asgi_application function to set up the ASGI application
from django.core.asgi import get_asgi_application

# Set the default settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')

# Create the ASGI application callable
application = get_asgi_application()
