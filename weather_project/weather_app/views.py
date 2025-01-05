# Import the render function to render templates
from django.shortcuts import render

# Import the datetime module to work with dates
import datetime

# Import the requests module to make HTTP requests
import requests

# Create views here.

# The index view handles both GET and POST requests
def index(request):
    # Read the API key from a file and remove any extra whitespace or newline characters
    API_KEY = open("API_KEY", "r").read().strip()
    
    # Define the API endpoint URLs for current weather and 5-day forecast
    current_weather_url = "http://api.weatherapi.com/v1/current.json?key={}&q={}"
    forecast_url = "http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=5"  # 5-day forecast
    
    # Handle the form submission when the request method is POST
    if request.method == "POST":
        # Get the first city from the form
        city1 = request.POST['city1']
        
        # Optionally get the second city, defaulting to None if not provided
        city2 = request.POST.get('city2', None)
        
        # Fetch weather and forecast data for the first city
        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
        
        # If a second city is provided, fetch its data; otherwise, set it to None
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None
        
        # Prepare the context dictionary with the fetched data
        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2
        }
        
        # Render the template with the context data
        return render(request, "weather_app/index.html", context)
    else:
        # If the request method is GET, render the template without context data
        return render(request, "weather_app/index.html")


# A helper function to fetch weather and forecast data for a given city
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetch current weather data by making a GET request to the weather API
    response = requests.get(current_weather_url.format(api_key, city)).json()
    
    # Extract the relevant current weather information
    weather_data = {
        "city": city,  # City name
        "temperature": response['current']['temp_c'],  # Current temperature in Celsius
        "description": response['current']['condition']['text'],  # Weather description
        "icon_url": response['current']['condition']['icon']  # Weather icon URL
    }
    
    # Fetch forecast data by making a GET request to the weather API
    forecast_response = requests.get(forecast_url.format(api_key, city)).json()
    
    # Initialize an empty list to store daily forecast information
    daily_forecasts = []
    
    # Loop through the forecast data for each day
    for daily_data in forecast_response['forecast']['forecastday']:
        # Append relevant forecast information for each day to the list
        daily_forecasts.append({
            "day": datetime.datetime.strptime(daily_data['date'], "%Y-%m-%d").strftime("%A"),  # Day of the week
            "min_temp": daily_data['day']['mintemp_c'],  # Minimum temperature in Celsius
            "max_temp": daily_data['day']['maxtemp_c'],  # Maximum temperature in Celsius
            "description": daily_data['day']['condition']['text'],  # Weather description
            "icon_url": daily_data['day']['condition']['icon']  # Weather icon URL
        })
    
    # Return the current weather data and the daily forecasts
    return weather_data, daily_forecasts
