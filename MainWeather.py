import webview
import tempfile
import python_weather
import pandas as pd
import folium
import asyncio
import branca
import tkinter as tk
from tkinter import messagebox, ttk
import os


#Load cities globally once
try:
    cities_df = pd.read_csv("WeatherMap/worldcities.csv")
    all_cities = sorted(cities_df['city'].dropna().unique().tolist())
except FileNotFoundError:
    all_cities = []
    messagebox.showerror("Error", "worldcities.csv file not found.")


# Fetches weather data asynchronously for the given city
async def fetch_weather(city):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        
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

# Helper function to add a pin to the map with weather information
def add_pin_to_map(lat, lon, weatherInfo, city_name):
    global map_obj

    if map_obj is None:
        map_obj = folium.Map(location=[lat, lon], zoom_start=4)

    df = pd.DataFrame(
    data=[[str(weatherInfo["temp"]) + " Degrees", "High: " + str(weatherInfo["highs"][1]), "High: " + str(weatherInfo["highs"][2])]
          , ["Feels like " + str(weatherInfo["feels"]) + " Degrees", "Low: " + str(weatherInfo["lows"][1]),  "Low: " +str(weatherInfo["lows"][2])]
          , ["High: " + str(weatherInfo["highs"][0]), "", ""]
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


    folium.Marker([lat, lon], popup=popup, tooltip=city_name).add_to(map_obj)

# Creates the map at given coordinates and puts weather in the popup
def generate_map(lat, long, weatherInfo):

    my_file = os.path.join(tempfile.gettempdir(), "map.html")  # Path to save the HTML map

    # Create the folium map
    my_map = folium.Map(location=[lat, long], zoom_start=12)
    
    # Create weather description for the popup
    df = pd.DataFrame(
    data=[[str(weatherInfo["temp"]) + " Degrees", "High: " + str(weatherInfo["highs"][1]), "High: " + str(weatherInfo["highs"][2])]
          , ["Feels like " + str(weatherInfo["feels"]) + " Degrees", "Low: " + str(weatherInfo["lows"][1]),  "Low: " +str(weatherInfo["lows"][2])]
          , ["High: " + str(weatherInfo["highs"][0]), "", ""]
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

def search_button_pressed(city):
    if city.strip() == "":
        messagebox.showerror("Error", "Please enter a city name.")
    else:
        try:
            df = pd.read_csv("WeatherMap/worldcities.csv")
            match = df[df["city"].str.lower() == city.strip().lower()]

            if match.empty:
                messagebox.showerror("Error", f"City '{city}' not found in the database.")
                return

            lat = float(match.iloc[0]["lat"])
            lon = float(match.iloc[0]["lng"])

            asyncio.run(main(city, lat, lon))
        except FileNotFoundError:
            messagebox.showerror("Error", "worldcities.csv file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexcpected error: {str(e)}")

#Entry filter
def on_city_typing(event):
    typed = city_var.get().lower()
    filtered = [c for c in all_cities if c.lower().startswith(typed)]
    city_box['values'] = filtered if filtered else all_cities

#Main for search window
def SearchWindow():
    global city_var, city_box

    main = tk.Tk()
    main.config(bg="#E4E2E2")
    main.title("Main Window")
    main.geometry("708x584")

    city_var = tk.StringVar()

    city_box = ttk.Combobox(main, textvariable=city_var)
    city_box.place(x=178, y=259, width=359, height=53)
    city_box['values'] = all_cities
    city_box.bind('<KeyRelease>', on_city_typing)

    search_button = tk.Button(master=main, text="Display Weather", command= lambda: search_button_pressed(city_var.get()))
    search_button.config(bg="#E4E2E2", fg="#000", )
    search_button.place(x=256, y=388, width=175, height=35)

    close_button = tk.Button(master=main, text="Close", command=main.destroy)
    close_button.config(bg="#E4E2E2", fg="#000", )
    close_button.place(x=256, y=470, width=175, height=35)

    main.mainloop()

# Entry point of the script
if __name__ == '__main__':
    SearchWindow()

