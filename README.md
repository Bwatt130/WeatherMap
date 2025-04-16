# WeatherMap
This is a final project that makes a weather forecast map for the CNSA-266 AM class.
Created by Alex Mansfield and Brandon Watson

To run the program:

    download and extract the MainWeather.zip file and run MainWeather.exe

The following list is a list of all the imported libraries that we used to make this project possible:

    webview
    tempfile
    python_weather
    pandas as pd
    folium
    asyncio
    branca
    tkinter as tk
    from tkinter import messagebox, ttk
    os

Overview:
    The main focus of the project revolves around Python_Weather, Folium, and Tkinter.

        Python-Weather is a python library that is able to pull local weather data by city name or coordinates.
        It is able to pull data from the current day, and up to 2 days in advance. It is also able to give hourly
        reports for the current day. The hourly reports will also display the forecast and rain percentage at each hour
        if desired.

        Folium is the library that generates maps based on coordinate points and can place pins and have adjustable zoom levels.
        The map can be fully interactive and creates a perfect stage for our weather map.

        Tkinter is the GUI standard for Python currently, and we decided to use it so we could condense our program
        into one application. Originally, we needed to use the user's browser to open the Folium map, but Tkinter gives
        a much more intuitive and convenient solution.

        The other libraries we used were mostly quality of life improvements to our code, being able to save us time
        in multiple instances. While the root of the project is possible without them, it overall functions best
        with them included.

Funtionality:
    The program works as follows:

        On launch, the list from worldcities.csv is preloaded. This is to allow the dropdown search to function properly.

        A Tkinter window is loaded with a search bar, a display weather button, and a close button. The search bars pulls cities
        from the worldcities.csv and displays their names to the user (coordinates are saved in the background.)

        Once the user enters a city into the search bar, they can click the display weather button. This button will check
        if the city entered into the search bar is a valid city to the ones we have in the .csv file. If it is
        invalid, a window will appear saying the city isn't recognized. If it valid, the coordinates associated with
        the city will be sent to Python Weather and Folium.

        Using the coordinates, a Folium map is generated with a pin on the city's location. When the pin is loaded onto
        the map, it is loaded with two HTML tables that pull data from the Python Weather library.

        The first table displays the forecast for the current day, and the next two days. It shows the current temperature
        for the current day, and the high and low forecasts for each of the three days.

        The second table contains the hourly forecast for the current day with the predicted temperature, and the weather status.

        Once done with the map, the user can close the window and continue searching for other cities if they choose. Otherwise,
        the close button will close the program.

Troubleshooting:
    While working on the project, we came across some road blocks:
        
        While we were initially using browsers to display the Folium map to the user, we struggled with actually getting the
        map to properly appear in the browser. As it turns out, opening the map in certain browsers doesn't play very nice.
        Our inital decision was to say that the application only works with Google Chrome, but we decided that was
        unrealistic and we needed to find a new solution that allowed for universal display. That's how we found out about Tkinter
        and we kept using it from there.

        With Tkinter, we wanted the search and the map to update within the same window, so it could be more dynamic, but as it
        turns out, Tkinter doesn't like trying to host dynamic web pages on it's own. We found out that we had to either pick user
        entry forms or the map to display per window, which lead us to using two windows: One for searching for cities, and the other
        for displaying the map/pin.

        Next, we needed a way to make it more convenient to find the cities that each user was searching for WITH their respective
        latitude and longitude coordinates. Thankfully, someone else had done all the work for us already, and after a quick search
        on the internet we found exactly what we were looking for in worldcities.csv. With this, we have a way to generate the map,
        search the weather, and allow the user to search for valid cities all in one.

        Now the issue is that Folium creates the map on the user's computer locally, and we needed to find a way that lets the
        application access the map regardless of the user's credentials. To do this, we thought it'd be best to use the user's
        temp directory in windows. The map does not take a lot of space, and it gets rewritten each time it is saved, so we don't need
        tons of storage or anything extravagant, we just need the map to be saved to a consistent place on every Windows computer.
        That being said, I should mention that this program will only operate on Windows systems because of this.

        The last major issue we had was how the program was presented to the user. To make this application more universal, we can't
        expect all of the users to already have all of the python libraries that we are using installed, or and IDE to use.
        Our work-around? Make the program into an executable file of course! What could possibly go wrong? (Cue not-so-subtle foreshadowing)

        To make our Python file into an .exe file, we need to use a python library called PyInstaller. Targeting our program with PyInstaller
        is all we need to do to get it saved as an .exe file, and from here on out, things stopped being easy. Since the program as being
        run as an application, it had more restrictive permissions than we were expecting. This made us rewrite how our map was saved, how
        the worldcities.csv file was read, and generally caused us an immense amount of exitential dread.

        After saving new versions of the program to .exe files around five different times, we finally had a version that worked on both
        of our systems without fault and lead to our project being in its current and complete state. 
        

    LOOK AT THIS IF YOU ARE ON WINDOWS 11

        The most notable issue we found was on Windows 11 systems, the .zip folder that the program and its dependencies are in will 
        need to be unblocked or else the drivers required to run the program will fail miserably. To do this:
            
            Right-click the .zip file

            Click into properties

            at the bottom, check the Unblock combo box
        
        And that's it! Believe it or not, it took us two whole days to figure that out...


Finally done:
    Overall, this was a pretty cool project that showed off practical python applications in a very easy-to-learn way. It was cool to create
    something and immediately see the use of the program as it developed. Even now after turning this in I still keep thinking of things we
    could improve on or refine in some way to make it a better user experience. Getting all of this done in 3-4 weeks while learning python 
    for the first time on top of it, I'd say we made a pretty cool project. Thank you for taking the time to read all of this if you did, and
    I hope you enjoy the project.