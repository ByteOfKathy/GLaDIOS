import commands
import geocoder

# def test_failing():
#     assert False


# def test_passing():
#     assert True


def test_weather():
    try:
        commands.fetchWeather("work")
    except ValueError as e:
        assert False, e.args[0]

    try:
        commands.fetchWeather("home")
    except ValueError as e:
        assert False, e.args[0]
    assert True


def test_email():
    try:
        commands.readEmails()
    except Exception as e:
        assert False, e.args[0]
    assert True


if __name__ == "__main__":
    pass
