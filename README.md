<p align="center">
<a href="https://www.python.org/downloads/release/python-3100/"><img alt="Python-3.10+" src="https://img.shields.io/badge/Python-3.10+-<COLOR>.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# GLaDIOS

My personal home assistant project to replace Alexa and Google Home. This project is heavily customized and tailored to my own needs, if you want to use it you will need to fork it and customize it to your needs.

Using Nerdaxic's tts [GLaDOS](https://github.com/nerdaxic/glados-tts)

## Requirements and Setup

### Google integration
You can skip this section if you do not want to use the google integration. (Reading emails, calendar events, and reading spreadsheet data)

You will need to have a `google_creds.json` file and supply your own credentials from [google](https://console.cloud.google.com/apis/credentials) in the main directory. It should be in the format:

```json
{
    "installed": {
        "client_id": "",
        "project_id": "",
        "auth_uri": "",
        "token_uri": "",
        "auth_provider_x509_cert_url": "",
        "client_secret": "",
        "redirect_uris": []
    }
}
```
### Setting up your environment variables

You will also need to supply `Gladios` with your own environment variables.

#### Open weather map

`WEATHER_KEY` - The key for [openweathermap](https://openweathermap.org/api)

#### Google

`EMAIL_PASS` - The key for your [gmail account] (https://myaccount.google.com/apppasswords)

`EMAIL_ADD` - Your gmail addre

## File explanations

### primary files

`commands.py` - The file with all the Gladios commands

`driver.py` - The file that drives the commands and wil be implemented on the raspberry pi

`engine.py` - the file that handles the tts on a hosted tts server

### folderws

`cache_common_tts` - the folder than contains cached common phrases that Gladios uses (mostly greetings and goodbyes)

### test files

`test_main.py` - The primary testing file for commands.py

### other

`requirments.txt` - The file that contains all the requirements for the project

`TTS-README.md` - Nerdaxic's readme for the tts

`models` - Nerdaxic's models for the tts

`.github` - workflow files for github actions

`utils` - Nerdaxic's utils for the tts

`xtraTypes.py` - TBD

## Running

| :warning: **Warning**: Only tested on Linux systems, WSL, and Windows |
| --------------------------------------------------------------------- |

1. Create your venv

ex: `python3 -m venv ./venv/`

2. Install the requirements

`pip install -r requirements.txt`

3. Install espeak on Linux

`sudo apt-get update -y`
`sudo apt-get install espeak -y`

4. Run

`python3 commands.py`

| :warning: **Warning**: This step is subject to change very soon |
| --------------------------------------------------------------- |

## Common issues

### espeak not found in windows
Sometimes Windows will not be able to find espeak, to fix this you will need to set the environment variable `PHONEMIZER_ESPEAK_LIBRARY` to the path of the espeak library. This can be done in the `commands.py` file by editing the following line:
```python
os.environ[
        "PHONEMIZER_ESPEAK_LIBRARY"
    ] = "Path/to/espeak.dll"
```

### WSL is slow
There is nothing I can do about this, it looks to be a WSL issue maybe with the drivers not being integrated very well. Any ideas/PRs would be welcome.