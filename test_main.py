import commands

# def test_failing():
#     assert False


def test_passing():
    assert True


def test_weather():
    try:
        commands.fetchWeather("work")
    except ValueError as e:
        assert False, e.args[0]

    try:
        commands.fetchWeather("home")
    except ValueError as e:
        assert False, e.args[0]
