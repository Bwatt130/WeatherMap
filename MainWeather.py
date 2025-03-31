import python_weather
import pandas as pd
import folium
import branca
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

    df = pd.DataFrame(
    data=[["apple", "oranges"], ["other", "stuff"]], columns=["cats", "dogs"]
    )

    html = df.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )

    popup = folium.Popup(html)

    iframe = branca.element.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)

    folium.Marker([40.7128, -74.0060], popup=popup).add_to(my_map)

    # Save the map as an HTML file
    map_filepath = "C:\Windows\Temp\map.html"
    my_map.save(map_filepath)

    # Open the HTML file in the user's default web browser using a popup window
    webbrowser.open(f"file:/{map_filepath}", new=2)

asyncio.run(getweather())
show_map_popup()