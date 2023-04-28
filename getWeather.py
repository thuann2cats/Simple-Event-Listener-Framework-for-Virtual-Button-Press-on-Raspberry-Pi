import requests
import json
import os
from speaker import Speaker

class WeatherForecast:
    def __init__(self, location):
        self.location = location
        self.sensor_hovered = False

    def speak(self, text):
        if not self.sensor_hovered:
            Speaker.speak(text)

    def getWeather(self):
        # set the API key and base URL for the OpenWeatherMap API
        api_key = "ca2b2481210be4d2c1674dce5d70e5ba"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        # combine the API key, base URL, and location to create the complete URL for the API request
        complete_url = base_url + "appid=" + api_key + "&q=" + self.location

        # send the API request and get the response
        response = requests.get(complete_url)

        # parse the JSON data from the response
        x = response.json()

        # if the "cod" key in the JSON data is not "404" (i.e. the API request was successful)
        if x["cod"] != "404":
            # extract the temperature, humidity, and weather description from the JSON data
            y = x["main"]
            current_temperature_kelvin = y["temp"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            # convert the temperature from Kelvin to Celsius
            current_temperature_celsius = round(current_temperature_kelvin - 273.15, 2)

            # print out the weather information for the location
            return (f"The temperature in {self.location} is {current_temperature_celsius} Celsius, humidity is {current_humidity}% and the weather is described as {weather_description}.")

            # speak the weather information
            # text = f"Here's today's weather: The temperature in {self.location} is {current_temperature_celsius} Celsius. The humidity is {current_humidity}%. The weather is described as {weather_description}."
            # self.speak(text)
        else:
            # if the API request was unsuccessful, print an error message
            return f"Could not retrieve weather information for {self.location}."
            
    def hoverSensor(self, is_hovered):
        self.sensor_hovered = is_hovered