# main loop program to drive any commands

import commands
from glados import glados_speak
import random
import speech_recognition as sr
import pyaudio
import time
import wave
import threading
import os
from pixels import Pixels
import valib
import response
from dotenv import load_dotenv

# settings for gladios wakeword
WAKEWORD = "glados"

# setup for mic pickup I'm using
# TODO: include mic setup in README
load_dotenv("sys.env")

# example system env variables
# RESPEAKER_RATE = 44100                  # Sample rate of the mic.
# RESPEAKER_CHANNELS = 1                  # Number of channel of the input device.
# RESPEAKER_WIDTH = 2
# RESPEAKER_INDEX = 0                     # run the check_device_id.py to get the mic index.
# CHUNK = 1024                            # Number of frames per buffer.
# WAVE_OUTPUT_FILEPATH = "/mnt/ramdisk/"

r = sr.Recognizer()
load_dotenv("sys.env")


class voiceProcessor(object):
    """
    Class to handle voice recognition
    """

    def __init__(self, isMuted=False):
        """
        create pyaudio instance
        """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            rate=os.environ["RESPEAKER_RATE"],
            format=pyaudio.paInt16,
            input_device_index=int(os.environ["RESPEAKER_INDEX"]),
            channels=os.environ["RESPEAKER_CHANNELS"],
            input=True,
            frames_per_buffer=os.environ["CHUNK"],
        )
        self.isMuted = isMuted

    def voiceCommandProcess(self, file: str, wait_time=3) -> str:
        # delete the file if it exists
        if os.path.exists(file):
            os.remove(file)
        # record audio to a new file
        with sr.AudioFile(file) as source:
            r.adjust_for_ambient_noise(source=source, duration=0.5)
            while wait_time > 0:
                audio = r.record(source, duration=3)
                # if we have the audio, we can break out of the loop
                if audio:
                    break
                # otherwise, we decrement the wait time
                wait_time -= 1
                time.sleep(1)
            # if we have audio, we can process it
            if audio:
                try:
                    recog_text = r.recognize_google(audio)
                    # print(recog_text)
                # except any errors
                except sr.UnknownValueError or sr.RequestError as e:
                    print(str(e))
                    os.remove(file)
                    return ""
            return recog_text


# initialize pixels
px = Pixels()
vHandler = voiceProcessor()
# test run px
px.wakeup()
time.sleep(1)
px.off()

if __name__ == "__main__":
    while True:
        # wait for wake word
        while not vHandler.isMuted:
            if WAKEWORD in vHandler.voiceCommandProcess("process.wav").lower():
                # select a random greeting from ./cache_common_tts folder and play it
                greeting = random.choice(os.listdir("./cache_common_tts"))
                os.system(f"aplay ./cache_common_tts/{greeting}")
                # listen for command
                recog_text = vHandler.voiceCommandProcess("process.wav").lower()
                # process command
                if (
                    "weather" in recog_text
                    or "temperature" in recog_text
                    or "forecast" in recog_text
                    or "conditions" in recog_text
                ):
                    commands.fetchWeather()
                elif "time" in recog_text or "date" in recog_text:
                    commands.fetchTime()
                elif "email" in recog_text:
                    commands.readEmails()
                elif (
                    "in my calendar" in recog_text or "calendar look like" in recog_text
                ):
                    commands.fetchCalendar()
                elif (
                    "food" in recog_text
                    or "lunch" in recog_text
                    or "dinner" in recog_text
                    or "menu" in recog_text
                ):
                    if [
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "tomorrow",
                    ] in recog_text:
                        # auto assume the last word is the day
                        commands.fetchFoodMenu(day=recog_text.strip(" ")[-1])
                    else:
                        commands.fetchFoodMenu()
                elif "help" in recog_text:
                    commands.help()
        # if glados is muted and we hear the wake word and unmute command
        if vHandler.isMuted and WAKEWORD in recog_text and "unmute" in recog_text:
            recog_text = vHandler.voiceCommandProcess("process.wav").lower()
            vHandler.isMuted = False

# shutdown procedure
px.off()
vHandler.stream.stop_stream()
vHandler.stream.close()
vHandler.p.terminate()
os.remove("process.wav")
