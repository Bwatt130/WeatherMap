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
def show_map_popup(lat, long):
    # Create a map object centered at a specific location
    my_map = folium.Map(location=[lat, long], zoom_start=10)  # Example: New York City

    df = pd.DataFrame(
    data=[["apple", "oranges"], ["other", "stuff"]], columns=["cats", "dogs"]
    )

    html = df.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )

    popup = folium.Popup(html)

    iframe = branca.element.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)

    folium.Marker([lat, long], popup=popup).add_to(my_map)

    # Save the map as an HTML file
    map_filepath = "C:\Windows\Temp\map.html"
    my_map.save(map_filepath)

    # Open the HTML file in the user's default web browser using a popup window
    webbrowser.open(f"file:/{map_filepath}", new=2)

asyncio.run(getweather())
m = folium.Map(location=(45.5236, -122.6750))
#show_map_popup(40.7128, -74.0060)

temp_dir = tempfile.gettempdir()
html_file_path = os.path.join(temp_dir, "map.html")

main = tk.Tk()
main.config(bg="#E4E2E2")
main.title("Main Window")
main.geometry("700x400")

label = tk.Label(master=main, text="Text Box")
label.config(bg="#E4E2E2", fg="#000")
label.place(x=57, y=76, width=80, height=40)

text = tk.Text(master=main)
text.config(bg="#fff", fg="#000")
text.place(x=60, y=154, width=120, height=80)

frame = HtmlFrame(main)
frame.load_website(html_file_path)
frame.pack(fill="both", expand=True)

main.mainloop()