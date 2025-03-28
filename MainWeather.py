import python_weather
import folium
import webbrowser
import asyncio
import os

async def getweather() -> None:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('Philadelphia')
    
        # returns the current day's forecast temperature (int)
        print(weather.temperature)
        
        # get the weather forecast for a few days
        for daily in weather:
            print(daily)
        
        # hourly forecasts
        for hourly in daily:
            print(f' --> {hourly!r}')
def show_map_popup():
    # Create a map object centered at a specific location
    my_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)  # Example: New York City

    chrome_path = '"C:\Program Files\Google\Chrome\Application\chrome.exe" %s'

    # Save the map as an HTML file
    map_filepath = "map.html"
    my_map.save(map_filepath)

    # Open the HTML file in a web browser using a popup window
    webbrowser.get(chrome_path).open(f"file://{map_filepath}", new=2)

asyncio.run(getweather())
m = folium.Map(location=(45.5236, -122.6750))
show_map_popup()