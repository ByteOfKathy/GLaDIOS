from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os


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
                print(
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
        autoDay = True
    elif day not in days:
        print(
            "You gave me an invalid day. Science has now validated your birth mother's decision to abandon you at CLO"
        )
        return
    # if the time is past 6pm, then we want to get the menu for the next day
    if datetime.now().hour > 18 and autoDay:
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
        print("well, looks like there are no cakes nor food today")
        return
    # TODO: cache the menu to a file to see if we need to fetch the menu again or if it has changed over the weekend

    # read the menu
    # check if the time is before 2pm
    if datetime.now().hour < 14:
        print("Today's lunch menu is")
        # read lunch menu based on the index of the day
        for i in range(4):
            print(values[i][days.index(day)])
    print("Today's dinner menu is")
    # read dinner menu based on the index of the day
    for i in range(6, 9):
        print(values[i][days.index(day)])


if __name__ == "__main__":
    os.getenv("secrets.env")
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    fetchFoodMenu()
