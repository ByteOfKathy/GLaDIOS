import commands
import datetime as dt

# used to test if pytest will run

# def test_failing():
#     assert False


# def test_passing():
#     assert True

# deprecating until fetchWeather gets static location integration from me
"""
def test_fetchWeather():
    try:
        commands.fetchWeather("work")
    except ValueError as e:
        assert False, e.args[0]

    try:
        commands.fetchWeather("home")
    except ValueError as e:
        assert False, e.args[0]
    assert True
"""


def test_fetchWeather():
    try:
        commands.fetchWeather()
    except Exception as e:
        assert False, e.args[0]
    assert True


def xtest_loginCalendar():
    try:
        commands.loginCalendar()
    except Exception as e:
        assert False, e.args[0]
    assert True


def xtest_readEmails():
    try:
        commands.readEmails(True)
    except Exception as e:
        assert False, e.args[0]
    assert True


def xtest_fetchCalender():
    try:
        commands.fetchCalender()
    except Exception as e:
        assert False, e.args[0]
    assert True


def xtest_addEventCalendar():
    try:
        # add an event to the calendar specifying the start date and start time as now
        commands.addEventCalendar("Test Event", dt.datetime.now(), dt.datetime.now())
    except Exception as e:
        assert False, e.args[0]
    assert True


if __name__ == "__main__":
    pass
