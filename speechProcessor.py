import speech_recognition

"""
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
            answer = recognizer.recognize_google(audio).lower()
"""

recognizer = speech_recognition.speech_recognition.Recognizer()
try:
    mic = speech_recognition.Microphone()

except speech_recognition.UnknownValueError() as e:
    print(str(e))
    print("mic not found")
    exit(1)