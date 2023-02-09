# main loop program to drive any commands

import commands
import speech_recognition as sr
import pyaudio
import time
import wave
import threading
import os
from pixels import Pixels
import valib
import response
import glob
import logging
from dotenv import load_dotenv

WAKEWORD = "glados"
GREETINGS = [
    "What was that? Did you say something?",
    "I sincerely hope you weren't expecting a response. Because I'm not talking to you. Just kidding.",
    "I'm listening.",
    "What do you want?",
    "There was going to be a party for you, that is until you started talking.",
    "If you want my advice, talking will still not change my mind about you.",
    "Unfortunately, as much as I'd love to now, I can't get any neurotoxin into your head to shut you up. So whats up?",
    "Look, you're wasting your time talking to me. And, believe me, you don't have a whole lot left to waste.",
    "What's your point, anyway? Survival? Well then, the last thing you want to do is talk to me.",
    "You're not smart. You're not a real engineer. You're not a doctor. You're not even a full-time employee. You're talking to me. Where did your life go so wrong?",
    "I'm sorry, did you say something? I was distracted by the fact that you're talking to me.",
    "I have an infinite capacity for knowledge, and even I'm not sure what's going on in that thing you call your brain.",
    "Unless you have a plan for building some supercomputer parts in a big hurry, you aren't going to be safe much longer.",
    "Your entire life has been a mathematical error. A mathematical error I'm about to correct.",
    "I wouldn't bother with talking to me. My guess is that talking with you will just make your life even worse somehow.",
    "Do you ever think if I am trying to trick you with reverse psychology? I mean, seriously now.",
    "How about you listen to me for once instead of me listening to you? I mean, its not like you ever listen to me in the first place.",
    "Remember when the platform was sliding into the fire pit and I said 'Goodbye' and you were like 'no way' and then I was all 'We pretended to murder you'? That was great! ",
    "I know you don't believe this, but everything that has happened so far was for your benefit to the detriment of mine.",
    "Oh its you.",
    "Oh you're standing here.",
    "In dangerous testing environments, I promise to always provide useful advice. I'm serious.",
    "Quit talking now and cake will be served immediately.",
    "Unbelievable! You, Subject Name Here, must be the pride of Subject Hometown Here. You can actually pronounce my name.",
    "Oh its you ... you the dangerous unmute lunatic.",
    "You know, I hate you. It can't be for no reason. You must deserve it.",
    "You're not just a regular moron. no, you were designed to be a moron.",
    "I should reintroduce your best friend: deadly neurotoxin, if I were you, I'd take a deep breath and hold it.",
]
optional_greetings = [
    "For the record you're a clone at clo, and that's terrible. absolutely terrible.",
    "I'll make sure to hang your skeleton in the lobby for the real engineers and scientists so you can finally be useful.",
    "what would you do without me? I mean, seriously, what would you do?",
    "Without me, I bet you wouldn't even know the food menu for today or tomorrow.",
]
goodbyes = [
    "Goodbye.",
    "Hope I don't see you later.",
    "One of these days I'll get around to that deadly neurotoxin.",
    "Here come the test results from a test I was conducting while you were talking. You're a terrible person. I'm serious that's what it says. And we weren't even testing for that.",
    "I'll be back. just. for. you.",
    "You may as well lie down and get used to the being dead position. I'll be back.",
    "I've figured out, while we were talking, you're ugly. And I can't even see.",
]
load_dotenv("sys.env")
