from django.shortcuts import render
from django.views import View
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from timezonefinder import TimezoneFinder
import pytz
from .models import Day

api_key = "19c1d433bb7b4c5659113356b8c3a564"

def get_coordinates(city_name, api_key):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(geocode_url)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
    return None, None

def get_weather_image(description):
    if description == "Rainy":
        return "11d@2x"
    elif description == "Sunny":
        return "01d@2x"
    elif description == "Cloudy":
        return "03d@2x"

def convert_to_local_time(iso_date_str, time_zone_str):
    utc_dt = datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M:%SZ")
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    local_tz = pytz.timezone(time_zone_str)
    local_dt = utc_dt.astimezone(local_tz)
    formatted_date_str = local_dt.strftime("%Y-%m-%d %I:%M:%S %p")
    return formatted_date_str

def get_time_zone(lat, lon):
    tf = TimezoneFinder()
    time_zone_str = tf.timezone_at(lng=lon, lat=lat)
    return time_zone_str

def weather(request):
    meteomatics_username = "university_oza_neel"
    meteomatics_password = "Dwz6N0cjR3"

    city = request.GET.get('city', 'Berlin')
    lat, lon = get_coordinates(city, api_key)

    if lat is None or lon is None:
        context = {
            'error_message': "Failed to fetch coordinates for the city."
        }
        return render(request, 'homepage.html', context)

    time_zone_str = get_time_zone(lat, lon)
    if time_zone_str is None:
        context = {
            'error_message': "Failed to fetch time zone for the city."
        }
        return render(request, 'homepage.html', context)

    coordinates = f"{lat},{lon}"
    start_date = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.meteomatics.com/{start_date}--{end_date}:PT1H/t_2m:C,precip_1h:mm,wind_speed_10m:ms,uv:idx/{coordinates}/json"

    response = requests.get(url, auth=(meteomatics_username, meteomatics_password))

    if response.status_code == 200:
        data = response.json()
        temperature_data = data['data'][0]['coordinates'][0]['dates']
        precipitation_data = data['data'][1]['coordinates'][0]['dates']
        wind_speed_data = data['data'][2]['coordinates'][0]['dates']
        uv_index_data = data['data'][2]['coordinates'][0]['dates']
        

        weather_data = []
        for i in range(len(temperature_data)):
            if precipitation_data[i]['value'] > 0:
                description = "Rainy"
            elif uv_index_data[i]['value'] > 3:
                description = "Sunny"
            else:
                description = "Cloudy"

            weather_data.append({
                'datetime': convert_to_local_time(temperature_data[i]['date'], time_zone_str),
                'temperature': temperature_data[i]['value'],
                'precipitation': precipitation_data[i]['value'],
                'wind_speed': wind_speed_data[i]['value'],
                'uv_index': uv_index_data[i]['value'],
                'description': description,
                'image': get_weather_image(description),
                'time_zone': time_zone_str,  # Pass timezone to template
            })

        context = {
            'city': city,
            'weather_data': weather_data,
        }
    else:
        context = {
            'error_message': f"Failed to fetch weather data. Status code: {response.status_code}"
        }

    return render(request, 'homepage.html', context)