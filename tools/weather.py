import requests

def get_grid(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1
    }

    response = requests.get(url, params=params)
    
    data = response.json()

    if "results" not in data:
        # City not found
        return None

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]

    return lat, lon

def get_weather(lat,lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":lat,
        "longitude":lon,
        "current_weather":True
        }
    response=requests.get(url,params=params)
    if response.status_code != 200:
        return None
    data=response.json()
    temp = data["current_weather"]["temperature"]
    ftemp = temp*9/5+32
    return ftemp


def weather_tool(city):
    coords = get_grid(city)

    if coords is None:
        return None
    lat, lon = coords
    weather = get_weather(lat, lon)

    if weather is None:
        return "Weather service unavailable."
    
    return weather

def weather_script(ai_name, user_name, city):
    if not city or not city.strip():
        return f"{ai_name}: Usage: /weather <city>"
    result = weather_tool(city)
    if result is None:
        return f"{ai_name}: City not found or weather service unavailable."
    return(f"{ai_name}: The temperature in {city} is {result}°F.")
