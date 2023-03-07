import commands
import datetime as dt
import pytest

# This file is used to test the commands.py file locally
# TODO: add secrets to github actions


# deprecating until fetchWeather gets static location integration from me and I can log the secrets
@pytest.mark.skip
def test_fetchWeatherLocations():
    try:
        commands.fetchWeather("work")
    except ValueError as e:
        assert False, e.args[0]

    try:
        commands.fetchWeather("home")
    except ValueError as e:
        assert False, e.args[0]
    assert True


def test_fetchWeather():
    try:
        commands.fetchWeather()
    except Exception as e:
        assert False, e.args[0]
    assert True


@pytest.mark.skip
def test_loginCalendar():
    try:
        commands.loginCalendar()
    except Exception as e:
        assert False, e.args[0]
    assert True


@pytest.mark.skip
def test_readEmails():
    try:
        commands.readEmails(True)
    except Exception as e:
        assert False, e.args[0]
    assert True


def test_fetchCalender():
    try:
        commands.fetchCalendar()
    except Exception as e:
        assert False, e.args[0]
    assert True


@pytest.mark.skip
def test_addEventCalendar():
    try:
        # add an event to the calendar specifying the start date and start time as now
        commands.addEventCalendar("Test Event", dt.datetime.now(), dt.datetime.now())
    except Exception as e:
        assert False, e.args[0]
    assert True


def test_fetchTime():
    try:
        commands.fetchTime()
    except Exception as e:
        assert False, e.args[0]
    assert True

def test_remind():


if __name__ == "__main__":
    pass
