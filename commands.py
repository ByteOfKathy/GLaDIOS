import os
from unicodedata import name
import requests
from dotenv import load_dotenv

load_dotenv("secrets.env")
wkey = os.getenv("WEATHER_KEY")


def fetchWeather(loc: str):
    """
    Fetches the weather for a given location.
    """
    if loc == "work":
        lat = os.getenv("WORK_LAT")
        lon = os.getenv("WORK_LON")
    elif loc == "home":
        lat = os.getenv("HOME_LAT")
        lon = os.getenv("HOME_LON")
    else:
        raise ValueError("Invalid location")
    url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=minutely,hourly,alerts&appid={}".format(
        lat, lon, wkey
    )
    response = requests.get(url)
    data = response.json()
    try:
        temp = data["current"]["temp"]
        feelslike = data["current"]["feels_like"]
        weather = data["current"]["weather"][0]["description"]
        maxTemp = data["daily"][0]["temp"]["max"]
        minTemp = data["daily"][0]["temp"]["min"]
    except KeyError as e:
        raise ValueError("Invalid response from API") from e

    ret = """It is currently {} degrees but feels like {} The weather is {}. The high today is {} and the low is {}.
             You would know that if you went outside and actually touched grass.""".format(
        temp, feelslike, weather, maxTemp, minTemp
    )
    return ret


def toggleLight():
    pass


if __name__ == "__main__":
    fetchWeather("work")
    fetchWeather("home")
