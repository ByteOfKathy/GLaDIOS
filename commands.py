import datetime
import os
from dotenv import load_dotenv
from glados import glados_speak

# read emails
import imaplib
import email
import requests

# location integration
import geocoder

# calendar integration
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv("secrets.env")


def fetchWeather():
    """
    Fetches the weather for your ip address.
    """
    loc = geocoder.ip("me")
    lat, lon = loc.latlng

    if not lat or not lon:
        raise ValueError("Invalid location")
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

    ret = "It is currently {} degrees. and feels like {} degrees. The weather is. {}. The high today is {} degrees. and the low is {} degrees. You would know that if you went outside and actually touched grass.".format(
        temp, feelslike, weather, maxTemp, minTemp
    )
    if "rain" in dailyWeather:
        ret += ".. Well on second thought maybe dont touch grass today. Your circuits might fry in the rain."
    glados_speak(ret)


def readEmails():
    """
    Reads unread emails from your inbox.
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
            # delete/skip the email
            glados_speak("Would you like to delete or skip the email?")
            answer = input("d/s: ")
            if answer == "d":
                mail.store(i, "+FLAGS", "\\Deleted")

            glados_speak("fetching next email...")
        glados_speak("Well... that looks like all the emails. You monster.")
    else:
        glados_speak("No unread emails. You monster.")
    mail.close()
    mail.logout()


# TODO: calendar integration with google
def loginCalendar() -> Credentials:
    """
    Logs into your calendar.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", scopes=["https://www.googleapis.com/auth/calendar"]
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_creds.json", scopes=["https://www.googleapis.com/auth/calendar"]
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


# TODO: test this
def fetchCalendar():
    """
    Fetches the calendar for your account.
    """
    creds = loginCalendar()
    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
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
        glados_speak("At {}. You have. {}".format(start, event["summary"]))
        # TODO: prompt the user to list the next event, delete the current event, or stop listing events
        # service.events().delete(calendarId="primary", eventId=event["id"]).execute() code to delete event
    glados_speak(
        "Well... that looks like the next set of events. and Remember the Aperture Science Bring Your Daughter to Work Day is the perfect time to have her tested"
    )


def addEventCalendar(summary: str, startDate: str, startTime: str):
    """
    Adds an event to your calendar.
    """
    creds = loginCalendar()
    # store the start startDate, startTime, and endTime in a datetime object
    endTime = datetime.datetime.strptime(startTime, "%H:%M") + datetime.timedelta(
        hours=1
    )
    dTime = datetime.datetime.strptime(
        "{} {}".format(startDate, startTime), "%Y-%m-%dT%H:%M"
    )

    # login to calendar and create event
    creds = loginCalendar()
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": summary,
        "start": {
            "dateTime": "{}-{}".format(
                dTime.strftime("%Y-%m-%dT%H:%M"), endTime.strftime("%H:%M")
            ),
            "timeZone": "America/New_York",
        },
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    glados_speak(
        "Event created. You might want to check your calendar. Cake, and grief counseling, will be available upon checking."
    )


# TODO: light integration
def toggleLight():
    pass


# TODO: ledger app integration
def addToLedger():
    """
    Adds an entry to your ledger.
    """
    pass


def removeFromLedger():
    """
    Removes an entry from your ledger.
    """
    pass


# main to test functions
if __name__ == "__main__":
    # fetchWeather("work")
    # fetchWeather()

    # readEmails()
    loginCalendar()
    pass
