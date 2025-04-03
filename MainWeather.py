import webview
import tempfile
import python_weather
import folium
import asyncio
import os

<<<<<<< HEAD
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
=======
# Make different functions for creating weather object, getting daily forecasts, getting todays hourly forecasts
# weather object creates weather forecast based on user input
# daily forecasts returns the highs and lows of the next 3 days as 2d array (and maybe description if possible)
# hourly forecast returns temp and desc of weather in 3 hour intervals in 2d array

#daily and hourly will call create at the start of each.

async def getweather():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('Philadelphia')
        print(weather.daily_forecasts[0].highest_temperature)
        print(weather.daily_forecasts[0].lowest_temperature)
    
        # returns the current day's forecast temperature (int)
        print(str(weather.temperature) + " degrees. Feels like " + str(weather.feels_like) + " degrees")
        
        # get the weather forecast for 3 days
        # gets highs and lows of temp
        highs = []
        lows = []
        dates = []
        for daily in weather:
            highs.append(daily.highest_temperature)
            lows.append(daily.lowest_temperature)
            dates.append(daily.date)
        print(highs) #WANT TO RETURN
        print(lows) #WANT TO RETURN
        
        # hourly forecasts every 3 hours
        today = []
        desc = []
        for hourly in daily:
            today.append(hourly.temperature)
            desc.append(hourly.description)
        print(today) #WANT TO RETURN
        print(desc) #WANT TO RETURN
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
>>>>>>> bda91082e528f74a6b0996a0b38919e3a9ce17fb

# Creates the map at given coordinates and puts weather in the popup
def generate_map(lat, lon, weather_info):
    map_file = os.path.join(tempfile.gettempdir(), "map.html")  # Path to save the HTML map

<<<<<<< HEAD
    # Create weather description for the popup
    popup_html = f"""
    <b>Today's Weather:</b><br>
    Temp: {weather_info['temperature']}°F (Feels like {weather_info['feels_like']}°F)<br>
    High: {weather_info['high']}°F, Low: {weather_info['low']}°F<br>
    Condition: {weather_info['description']}
    """

    # Create the folium map
    folium_map = folium.Map(location=[lat, lon], zoom_start=12)
=======
    df = pd.DataFrame(
    data=[[str(weatherInfo["temp"]) + " Degrees", "High: " + str(weatherInfo["highs"][1]), "High: " + str(weatherInfo["highs"][2])]
          , ["Feels like " + str(weatherInfo["feels"]) + " Degrees", "Low: " + str(weatherInfo["lows"][1]),  "Low: " +str(weatherInfo["lows"][2])]
          , ["High: " + str(weatherInfo["highs"][0]), "tomorrow desc", "aftermorrow desc"]
          , ["Low: " + str(weatherInfo["lows"][0]),"",""]]
          , columns=["Today", weatherInfo["dates"][1],weatherInfo["dates"][2]]
    )

    html = df.to_html(
        classes="table table-striped table-hover table-responsive",
        index=False,
        justify="left"
    )
>>>>>>> bda91082e528f74a6b0996a0b38919e3a9ce17fb

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

<<<<<<< HEAD
# Entry point of the script
if __name__ == '__main__':
    asyncio.run(main('Philadelphia', 39.9526, -75.1652))
=======
    #openWindow(map_filepath)

    # Open the HTML file in the user's default web browser using a popup window
    webbrowser.open(f"file:/{map_filepath}", new=2)

def openWindow(filepath):
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
    frame.load_file(filepath)
    print(filepath)
    frame.pack(fill="both", expand=True)

    main.mainloop()

weatherInfo = asyncio.run(getweather())
m = folium.Map(location=(45.5236, -122.6750))
createMap(40.7128, -74.0060, weatherInfo)
>>>>>>> bda91082e528f74a6b0996a0b38919e3a9ce17fb
