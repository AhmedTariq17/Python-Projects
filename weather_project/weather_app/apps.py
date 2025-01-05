# Import the AppConfig class from the Django apps module
from django.apps import AppConfig


# Define the configuration class for the weather application
class WeatherAppConfig(AppConfig):
    # Specify the default type of primary key to be used for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Set the name of the application. This should match the name of the app's folder
    name = 'weather_app'
