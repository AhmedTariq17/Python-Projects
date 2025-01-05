# Import the path function from Django's urls module
from django.urls import path

# Import the views module from the current directory
from . import views

# Define the URL patterns for this application
urlpatterns = [
    # Map the root URL ('') to the 'index' view function in the views module
    # The 'name' parameter assigns a name ('index') to this URL pattern for reference in templates and code
    path('', views.index, name='index'),
]
