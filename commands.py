from asyncore import read
import os
import imaplib
import email
from unicodedata import name
import requests
from dotenv import load_dotenv
from glados import glados_speak

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
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly,alerts&units=imperial&appid={}".format(
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

    ret = "It is currently {} degrees. and feels like {} degrees. The weather is. {}. The high today is {}. and the low is {}. You would know that if you went outside and actually touched grass.".format(
        temp, feelslike, weather, maxTemp, minTemp
    )

    glados_speak(ret)


def toggleLight():
    pass


def nextClass():
    pass


def editClass():
    pass


def readEmails():
    """
    Reads unread emails from the inbox.
    """
    # Connect to the inbox
    glados_speak("Connecting to your inbox...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv("EMAIL_ADD"), os.getenv("EMAIL_PASS"))
    mail.select("inbox")
    _, data = mail.search(None, "UNSEEN")
    ids = data[0]
    id_list = ids.split()
    if len(id_list) > 0:
        glados_speak("Reading your emails...")
        for i in id_list:
            _, data = mail.fetch(i, "(RFC822)")
            raw = data[0][1]
            msg = email.message_from_bytes(raw)
            glados_speak("email from {} about {}.".format(msg["from"], msg["subject"]))
            """
            # TODO: Read the email and respond accordingly
            answer = input("y/n: ")
            if answer == "y":
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        glados_speak(str(body).strip())
                mail.store(i, "+FLAGS", "\\Seen")
            """
            glados_speak("fetching next email...")
        glados_speak("Well... that looks like all the emails. You monster.")
    else:
        glados_speak("No unread emails. You monster.")


if __name__ == "__main__":
    # fetchWeather("work")
    # fetchWeather("home")

    # readEmails()
