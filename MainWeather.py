import tkinter as tk
from tkinterweb import HtmlFrame
import tempfile
import python_weather
import pandas as pd
import folium
import branca
import webbrowser
import asyncio
import os

async def getweather():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('Philadelphia')
        
        # get the weather forecast for 3 days
        # gets highs and lows of temp
        highs = []
        lows = []
        dates = []
        for daily in weather:
            highs.append(daily.highest_temperature)
            lows.append(daily.lowest_temperature)
            dates.append(daily.date)
        
        # hourly forecasts every 3 hours
        today = []
        desc = []
        for hourly in daily:
            today.append(hourly.temperature)
            desc.append(hourly.description)
        return{
            "temp": weather.temperature,
            "feels": weather.feels_like,
            "highs": highs,
            "lows": lows,
            "today": today,
            "desc": desc,
            "dates": dates
        }
        
def createMap(lat, long, weatherInfo):
    # Create a map object centered at a specific location
    my_map = folium.Map(location=[lat, long], zoom_start=10)  # Example: New York City

    #Search .csv file for coords
    #Get city and send to getweather()

    df = pd.DataFrame(
    data=[[str(weatherInfo["temp"]) + " Degrees", "High: " + str(weatherInfo["highs"][1]), "High: " + str(weatherInfo["highs"][2])]
          , ["Feels like " + str(weatherInfo["feels"]) + " Degrees", "Low: " + str(weatherInfo["lows"][1]),  "Low: " +str(weatherInfo["lows"][2])]
          , ["High: " + str(weatherInfo["highs"][0]), "tomorrow desc", "aftermorrow desc"]
          , ["Low: " + str(weatherInfo["lows"][0]),"",""]]
          , columns=["Today", weatherInfo["dates"][1],weatherInfo["dates"][2]]
    )
    
    df2 = pd.DataFrame(
    data=[[str(weatherInfo["today"][0]), str(weatherInfo["today"][1]), str(weatherInfo["today"][2]), str(weatherInfo["today"][3]), str(weatherInfo["today"][4]), str(weatherInfo["today"][5]), str(weatherInfo["today"][6]), str(weatherInfo["today"][7])]
        ,  [weatherInfo["desc"][0],weatherInfo["desc"][1],weatherInfo["desc"][2],weatherInfo["desc"][3],weatherInfo["desc"][4],weatherInfo["desc"][5],weatherInfo["desc"][6],weatherInfo["desc"][7]]]
        , columns=["12am", "3am", "6am", "9am", "12pm", "3pm", "6pm", "9pm"]
    )

    forecasthtml = df.to_html(
        classes="table table-striped table-hover table-responsive",
        index=False,
        justify="left"
    )

    hourlyhtml = df2.to_html(
        classes="table table-striped table-hover table-responsive",
        index=False,
        justify="left"
    )

    html = forecasthtml + "<br>" + hourlyhtml

    popup = folium.Popup(html)

    iframe = branca.element.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)

    folium.Marker([lat, long], popup=popup).add_to(my_map)

    # Save the map as an HTML file
    map_filepath = r"C:\Windows\Temp\map.html"
    my_map.save(map_filepath)

    #openWindow(map_filepath)

    # Open the HTML file in the user's default web browser using a popup window
    webbrowser.open(f"file:/{map_filepath}", new=2)

weatherInfo = asyncio.run(getweather())
m = folium.Map(location=(45.5236, -122.6750))
createMap(40.7128, -74.0060, weatherInfo)