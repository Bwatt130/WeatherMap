import webview
import tempfile
import python_weather
import folium
import asyncio
import os

# Fetches weather data asynchronously for the given city
async def fetch_weather(city='Philadelphia'):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        return {
            'temperature': weather.temperature,
            'feels_like': weather.feels_like,
            'high': weather.daily_forecasts[0].highest_temperature,
            'low': weather.daily_forecasts[0].lowest_temperature,
            'description': weather.description
        }

# Creates the map at given coordinates and puts weather in the popup
def generate_map(lat, lon, weather_info):
    map_file = os.path.join(tempfile.gettempdir(), "map.html")  # Path to save the HTML map

    # Create weather description for the popup
    popup_html = f"""
    <b>Today's Weather:</b><br>
    Temp: {weather_info['temperature']}°F (Feels like {weather_info['feels_like']}°F)<br>
    High: {weather_info['high']}°F, Low: {weather_info['low']}°F<br>
    Condition: {weather_info['description']}
    """

    # Create the folium map
    folium_map = folium.Map(location=[lat, lon], zoom_start=12)

    # Add marker with weather popup and tooltip
    folium.Marker(
        [lat, lon],
        popup=popup_html,
        tooltip="Click for weather"
    ).add_to(folium_map)

    folium_map.save(map_file)  # Save map to file
    return map_file

# Main function to coordinate map creation and display in webview
async def main(city, lat, lon):
    weather_info = await fetch_weather(city)  # Get weather data
    map_file = generate_map(lat, lon, weather_info)  # Generate map with weather in popup

    # Start the webview GUI with the map file
    window = webview.create_window("Weather & Map Viewer", map_file, width=800, height=600)
    webview.start()  # No custom load function needed now

# Entry point of the script
if __name__ == '__main__':
    asyncio.run(main('Philadelphia', 39.9526, -75.1652))
