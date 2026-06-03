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
        print("City not found")
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

def main():
    city = input("City: ")
    coords=get_grid(city)
    if coords is None:
        return
    lat,lon = coords
    get_weather(lat,lon)
    

def weather_tool(city):
    coords = get_grid(city)

    if coords is None:
        return
    lat, lon = coords
    weather = get_weather(lat, lon)

    if weather is None:
        return "Weather service unavailable."
    
    return f"The temperature in {city} is {weather}°F."

def weather_script(ai_name, city):
    print()
    print(f"{ai_name}: Thinking...")
    print()
    print(f"{ai_name}:", weather_tool(city))
    print()
