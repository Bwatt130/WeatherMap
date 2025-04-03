import webview
import tempfile
import python_weather
import pandas as pd
import folium
import asyncio
import branca
import os

# Fetches weather data asynchronously for the given city
async def fetch_weather(city):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
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

# Creates the map at given coordinates and puts weather in the popup
def generate_map(lat, long, weatherInfo):

    my_file = os.path.join(tempfile.gettempdir(), "map.html")  # Path to save the HTML map

    # Create the folium map
    my_map = folium.Map(location=[lat, long], zoom_start=12)
    
    # Create weather description for the popup
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

    popup = folium.Popup(html)

    iframe = branca.element.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)


    # Add marker with weather popup and tooltip
    folium.Marker([lat, long], popup=popup).add_to(my_map)

    my_map.save(my_file)  # Save map to file
    return my_file

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
