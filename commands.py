import datetime
import os
import random
from datetime import time, timedelta
import pytz
from datetime import datetime
from dotenv import load_dotenv
from glados import glados_speak

# custom types
import xtraTypes

# read emails
import imaplib
import email
import requests

# location integration
import geocoder

# calendar integration
import calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv("secrets.env")


def is_dst(dt=None, timezone="UTC"):
    """
    tests if a given datetime or the current time is in daylight savings time or not.

    Parameters
    ----------
    dt: datetime
        The datetime to test. If none, will use the current time.
    timezone: str
        The timezone to test. If none, will use UTC.
    """
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


def fetchWeather(location: str):
    """
    Fetches the weather for a given physical address or your ip address.

    Parameters
    ----------
    location: str
        The physical address to fetch the weather for.
    """
    loc = geocoder.osm(location) if location else geocoder.ipinfo("me")
    lat, lon = loc.latlng

    url = "https://api.openweathermap.org/data/2.5/onecall?lat={:0.2f}&lon={:0.2f}&exclude=minutely,hourly,alerts&units=imperial&appid={}".format(
        lat, lon, os.getenv("WEATHER_KEY")
    )
    response = requests.get(url)
    data = response.json()
    try:
        temp = round(data["current"]["temp"])
        feelslike = round(data["current"]["feels_like"])
        weather = data["current"]["weather"][0]["description"]
        dailyWeather = data["daily"][0]["weather"][0]["description"]
        maxTemp = round(data["daily"][0]["temp"]["max"])
        minTemp = round(data["daily"][0]["temp"]["min"])
    except KeyError as e:
        raise ValueError("Invalid response from API") from e
    ret = "Using Fahrenheit, It is currently {} degrees and feels like {} degrees. The weather is {}. The high today is {} degrees. and the low is {} degrees. You would know that if you went outside and actually touched grass.".format(
        temp, feelslike, weather, maxTemp, minTemp
    )
    if "rain" in weather:
        ret += ".. Well on second thought maybe dont touch grass today. Your circuits might fry in the rain."
    glados_speak(ret)


def readEmails(quickRead=True, timeframe=None):
    """
    Reads unread emails from your inbox based on the timeframe up to the next 10 events.

    Parameters
    ----------
    quickRead: bool
        If true, will only read the subject and sender of the email.
    timeframe: str
        The timeframe to look for emails. Valid timeframes are day, week, month.
    """
    validTimeframes = {
        "day": timedelta(days=1),
        "week": timedelta(weeks=1),
        "month": timedelta(days=31),
    }
    currentTime = datetime.now()
    if timeframe not in validTimeframes.keys():
        glados_speak(
            "You're not a good person. You know that, right? You couldn't even give a valid timeframe, so I decided to give you one."
        )
        timeframe = random.choice(list(validTimeframes.keys()))
    else:
        timeframe = validTimeframes[timeframe]
    # Connect to the inbox
    glados_speak("Connecting to your inbox...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv("EMAIL_ADD"), os.getenv("EMAIL_PASS"))
    mail.select("inbox")
    _, data = mail.search(None, "UNSEEN")
    ids = data[0]
    id_list = ids.split()
    if len(id_list) > 0:
        glados_speak("Accessing your emails...")
        emailNum = 0
        for i in id_list:
            if emailNum < 10:
                emailNum += 1
                _, data = mail.fetch(i, "(RFC822)")
                raw = data[0][1]
                msg = email.message_from_bytes(raw)
                glados_speak(
                    "email from {} about {}.".format(
                        msg["from"].split("@")[0], msg["subject"]
                    )
                )
                # TODO: remove the weird time zone stuff from the subject
                # print(msg["subject"])
                # TODO: test Read the email and respond accordingly
                if not quickRead:
                    glados_speak("would you like me to read it?")
                    answer = input("yes/no: ")
                    if answer == "yes":
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True)
                                glados_speak(str(body).strip())
                        # mail.store(i, "+FLAGS", "\\Seen")
            else:
                glados_speak(
                    "You have too many unread emails. I'm not going to read them all, do it yourself."
                )
                break

                # delete/skip the email
                glados_speak("Would you like to delete the email?")
                answer = input("yes/no: ")
                if answer == "yes":
                    mail.store(i, "+FLAGS", "\\Deleted")

        glados_speak(
            "Well... that looks like all the emails. Back to warming up the neurotoxin emitters ... cakes, I mean baking cakes"
        )
    else:
        glados_speak("Your inbox is empty and I'm all out of cake mix. Lucky you.")
    mail.close()
    mail.logout()


def loginGoogle() -> Credentials:
    """
    Refreshes google credentials if they are expired or creates new ones if they don't exist.
    Returns credentials if possible, otherwise none for an error
    """
    creds = None
    scopes = [
        "https://www.google.com/calendar/feeds",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            scopes=scopes,
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                glados_speak(
                    "How are you holding up? ... BECAUSE I'M A POTATO. THAT CAN'T ACCESS YOUR CALENDAR"
                )
                print(e)
                return
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_creds.json",
                scopes=scopes,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


# TODO: test this
def fetchCalendar():
    """
    Fetches the calendar for your account. Tells the next 5 events.
    """
    creds = loginGoogle()
    service = build("calendar", "v3", credentials=creds)
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        glados_speak("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        if "T" in start:
            # events that are not all day
            day = start.split("T")[0].split("-")[1:]
            hr, mins, _ = start[-14:-6].split(":")
            # clean up pronounciation of mins
            if mins == "00":
                mins = "O'clock"
            glados_speak(
                "On {} {}, at {} {} you have {}".format(
                    calendar.month_name[int(day[0])], day[1], hr, mins, event["summary"]
                )
            )
        else:
            # all day events
            day = start.split("-")[1:]
            glados_speak(
                "On {} {}, all day, you have {}".format(
                    calendar.month_name[int(day[0])], day[1], event["summary"]
                )
            )
        # TODO: prompt the user to delete the current event or stop listing events
        """
        glados_speak(
            "If you would like to stop or delete an event let me know or forever hold your grief cake"
        )
        recognizer.adjust_for_ambient_noise(mic, duration=0.5)
        audio = recognizer.listen(mic)
        answer = recognizer.recognize_google(audio).lower()
        
        time.sleep(1)
        answer = ""
        if answer == "delete":
            service.events().delete(calendarId="primary", eventId=event["id"]).execute()
        elif answer == "stop":
            return
        """
    glados_speak(
        "Well... that looks like the next set of events. and Remember the Aperture Science Bring Your Daughter to Work Day is the perfect time to have her tested"
    )


# TODO: test this
def addEventCalendar(summary: str, startDate: str):
    """
    Adds an event to your calendar.

    Parameters
    ----------
    summary : str
        The summary of the event
    startDate : str
        The start date of the event in the format YYYY-MM-DDTHH:MM
    """
    eTime = datetime.strptime(startDate, "%Y-%m-%dT%H:%M") + timedelta(hours=1)
    sTime = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
    # login to calendar and create event
    # TODO: daylight savings time
    creds = loginGoogle()
    if creds is None:
        return
    service = build("calendar", "v3", credentials=creds)
    offset = "04:00" if is_dst() else "05:00"
    event = {
        "summary": summary,
        "start": {
            "dateTime": "{}T{}:00-{}".format(
                sTime.strftime("%Y-%m-%d"), sTime.strftime("%H:%M"), offset
            ),
            "timeZone": "America/New_York",
        },
        "end": {
            "dateTime": "{}T{}:00-{}".format(
                eTime.strftime("%Y-%m-%d"), eTime.strftime("%H:%M"), offset
            ),
            "timeZone": "America/New_York",
        },
        "reminders": {
            "useDefault": True,
        },
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    glados_speak(
        "Event created. You might want to check your calendar. Cake, and grief counseling, will be available upon checking."
    )


# TODO: light integration
def toggleLight(state=xtraTypes.LightState.DEFAULT):
    # state overrides the current state of the light
    if state == xtraTypes.LightState.DEFAULT:
        # toggle the light
        pass
    elif state == xtraTypes.LightState.ON:
        # turn the light on
        pass
    elif state == xtraTypes.LightState.OFF:
        # turn the light off
        pass
    pass


def fetchTime():
    t = datetime.now().strftime("%H:%M")
    # if the minute is 0, then say o'clock instead
    if t[-2:] == "00":
        t = t[:-3] + "o clock"
    glados_speak("It is currently {}".format(t))


def fetchFoodMenu(day=""):
    """
    Fetches the food menu for the day.

    Parameters
    ----------
    day: the day of the week (monday, tuesday, wednesday, thursday, friday)
    """
    creds = loginGoogle()
    if not creds:
        return
    days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    if day == "":
        day = (
            days[datetime.now().weekday()] if datetime.now().weekday() < 5 else "monday"
        )
    elif day not in days and day != "tomorrow":
        glados_speak(
            "You gave me an invalid day. Science has now validated your birth mother's decision to abandon you at CLO"
        )
        return
    if day == "tomorrow":
        day = days[(datetime.now().weekday() + 1) % 5]
    # if the time is past 6pm, then we want to get the menu for the next day imply the user wants the menu for the next day
    if datetime.now().hour > 18:
        day = days[(days.index(day) + 1) % 5]
    spreadsheetId = "1xJdqjArlg1w6fZg9B0Z_5HZ69J62hkkgUqbWia5FZLs"
    sheetName = "menu"
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheetId, range="{}!B6:F15".format(sheetName))
        .execute()
    )
    values = result.get("values", [])
    if not values:
        glados_speak("well, looks like there are no cakes nor food today")
        return
    # TODO: cache the menu to a file to see if we need to fetch the menu again or if it has changed over the weekend

    # read the menu
    # check if the time is before 2pm
    if datetime.now().hour < 14:
        glados_speak("The lunch menu for {} is".format(day))
        # read lunch menu based on the index of the day
        for i in range(4):
            # if the value is not empty, then read it
            glados_speak(values[i][days.index(day)]) if values[i][
                days.index(day)
            ] != "" else None
    glados_speak("The dinner menu for {} is".format(day))
    # read dinner menu based on the index of the day
    for i in range(6, 9):
        # if the value is not empty, then read it
        glados_speak(values[i][days.index(day)]) if values[i][
            days.index(day)
        ] != "" else None


def remind(time, reason):
    """
    Reminds you of something at a certain time.
    """
    pass


def shutdownComputer(computer):
    """
    Shuts down a computer.
    """
    pass


# main to test functions
if __name__ == "__main__":
    # uncomment the function you want to test or better yet: run `pytest`

    # fetchWeather()

    # loginGoogle()

    # readEmails(timeframe="day")

    # fetchCalendar()

    # datetime format: "%Y-%m-%dT%H:%M"
    # addEventCalendar("test", "2023-02-01T11:00")

    # fetchTime()

    # fetchFoodMenu()
    # test tomorrow
    # fetchFoodMenu("tomorrow")
    # test invalid day
    # fetchFoodMenu("BLLLLLLLLLLLAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRGHHHHHH")

    # toggleLight(types.LightState.ON)
    # toggleLight(types.LightState.OFF)
    # toggleLight(types.LightState.DEFAULT)

    fetchTime()
    pass
