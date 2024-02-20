from django.shortcuts import render
import datetime
import requests

# Create your views here.
def index(request):
    API_KEY = open("API_KEY", "r").read().strip()  # .strip() removes any whitespace and newline characters
    current_weather_url = "http://api.weatherapi.com/v1/current.json?key={}&q={}"
    forecast_url = "http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=5" # Assuming a 5-day forecast

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")
    

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetching current weather data
    response = requests.get(current_weather_url.format(api_key, city)).json()
    # Assuming the icon URL is provided directly from the API response
    weather_data = {
        "city": city,
        "temperature": response['current']['temp_c'],
        "description": response['current']['condition']['text'],
        "icon_url": response['current']['condition']['icon']  # Use the full icon URL
    }

    # Fetching forecast data
    forecast_response = requests.get(forecast_url.format(api_key, city)).json()
    daily_forecasts = []
    for daily_data in forecast_response['forecast']['forecastday']:
        # Again, assuming the full icon URL is provided
        daily_forecasts.append({
            "day": datetime.datetime.strptime(daily_data['date'], "%Y-%m-%d").strftime("%A"),
            "min_temp": daily_data['day']['mintemp_c'],
            "max_temp": daily_data['day']['maxtemp_c'],
            "description": daily_data['day']['condition']['text'],
            "icon_url": daily_data['day']['condition']['icon']  # Use the full icon URL
        })

    return weather_data, daily_forecasts
