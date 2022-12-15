import commands

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


def test_readEmails():
    try:
        commands.readEmails(True)
    except Exception as e:
        assert False, e.args[0]
    assert True

def test_fetchCalender():
    


if __name__ == "__main__":
    pass
