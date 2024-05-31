import requests
import math

def get_coordinates(address):
    print(f"Fetching coordinates for address: {address}")
    api_key = "za-A1cq1tqqlOrxXrfn698tfJgC0m5CHW0s-nmYJDu8"
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        position = data['items'][0]['position']
        latitude = position['lat']
        longitude = position['lng']
        print(f"Coordinates fetched successfully: ({latitude}, {longitude})")
        return latitude, longitude
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def get_closest_weather_office(latitude, longitude):
    """
    Get information on the closest weather office using the provided GPS coordinates.
    """
    try:
        # Make request to /points/{latitude},{longitude} endpoint
        response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
        response.raise_for_status()
        data = response.json()

        # Extract weather office information
        office = data['properties']['cwa']
        grid_x = data['properties']['gridX']
        grid_y = data['properties']['gridY']

        return office, grid_x, grid_y
    except Exception as e:
        print(f"Error fetching weather office information: {e}")
        return None, None, None

def get_hourly_forecast(office, grid_x, grid_y):
    """
    Get the hourly weather forecast for the specified weather office and grid coordinates.
    """
    try:
        # Make request to /gridpoints/{office}/{grid_x},{grid_y}/forecast/ endpoint
        response = requests.get(f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast")
        response.raise_for_status()
        data = response.json()

        # Extract hourly forecast
        hourly_forecast = data['properties']['periods'][0]

        return hourly_forecast
    except Exception as e:
        print(f"Error fetching hourly forecast: {e}")
        return None

def fetch_weather_forecast(address):
    latitude, longitude = get_coordinates(address)

    if latitude is not None and longitude is not None:
        # Get information on the closest weather office
        office, grid_x, grid_y = get_closest_weather_office(latitude, longitude)
        if office:
            print(f"Closest weather office: {office}, Grid coordinates: ({grid_x}, {grid_y})")
            print("--------------------------")
            # Get hourly forecast for the weather office
            forecast = get_hourly_forecast(office, grid_x, grid_y)
            if forecast:
                print("Hourly Forecast:")
                print(f"{forecast['name']},{forecast['temperature']}°F,{forecast['shortForecast']},{forecast['icon']},{forecast['detailedForecast']}")
                momsays = []
                if 'Showers' in forecast['shortForecast'] or 'showers' in forecast['shortForecast']:
                    momsays.append("WEAR RAIN JACKET!")
                if 'sun' in forecast['shortForecast'].lower():
                    momsays.append("WEAR SUN HAT! and always remember you are my Sunshine")
                if 'thunderstorms' in forecast['shortForecast'].lower():
                    momsays.append("Don't hold a metal pole")
                if 'clear' in forecast['shortForecast'].lower():
                    momsays.append("I hope your mind is as clear as the sky!")
                momsays.append(" ")
                momsays.append(' ')
                print("Mom Says and you got to listen!")
                for advice in momsays:
                    print(advice)
                
                # Return forecast and mom's advice
                return forecast, momsays
            else:
                print("Failed to fetch hourly forecast.")
                return None, None
        else:
            print("Failed to fetch weather office information.")
            return None, None
    else:
        print("Failed to fetch coordinates.")
        return None, None

if __name__ == "__main__":
    address = "Empire state building, USA"  # You can change this address as needed
    forecast, advice = fetch_weather_forecast(address)
    if forecast:
        print(f"Forecast: {forecast}")
    if advice:
        print(f"Advice: {advice}")
