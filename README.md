<p align="center">
<a href="https://www.python.org/downloads/release/python-3100/"><img alt="Python-3.10+" src="https://img.shields.io/badge/Python-3.10+-<COLOR>.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# GLaDIOS

My personal home assistant project

Using Nerdaxic's tts [GLaDOS](https://github.com/nerdaxic/glados-tts)

## Requirements and Setup

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

You will also need to supply `Gladios` with your own environment variables.

`WEATHER_KEY` - The key for [openweathermap](https://openweathermap.org/api)

`EMAIL_PASS` - The key for your [gmail account](https://myaccount.google.com/apppasswords)

`EMAIL_ADD` - Your gmail address

`GLADIOS_GEOHOME` - A home address

`GLADIOS_GEOWORK` - A work address

## Running

| :warning: **Warning**: Only tested on Linux systems and WSL |
| --- |

1. Create your venv

`python3 -m venv ./venv/`

2. Install the requirements

`pip install -r requirements.txt`

3. Install espeak on Linux

`sudo apt-get update -y`
`sudo apt-get install espeak -y`

4. Run

`python3 commands.py`

| :warning: **Warning**: This step is subject to change very soon |
| --- |