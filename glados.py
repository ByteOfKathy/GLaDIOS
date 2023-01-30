import torch
from utils.tools import prepare_text
from scipy.io.wavfile import write
from sys import modules as mod

# from audioplayer import AudioPlayer
from phonemizer import phonemize
from phonemizer.separator import Separator
import os

try:
    import winsound
except ImportError:
    from subprocess import call

print("Initializing TTS Engine...")

# Select the device
if torch.is_vulkan_available():
    device = "vulkan"
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

# Load models
glados = torch.jit.load("models/glados.pt")
vocoder = torch.jit.load("models/vocoder-gpu.pt", map_location=device)

# Prepare models in RAM
for i in range(4):
    init = glados.generate_jit(prepare_text(str(i)))
    init_mel = init["mel_post"].to(device)
    init_vo = vocoder(init_mel)


def glados_speak(text: str):
    """
    generates audio from text and plays it
    """
    # Tokenize, clean and phonemize input text
    x = prepare_text(text).to("cpu")

    # Generate generic TTS-output
    tts_output = glados.generate_jit(x)

    # Use HiFiGAN as vocoder to make output sound like GLaDOS
    mel = tts_output["mel_post"].to(device)
    audio = vocoder(mel)

    # Normalize audio to fit in wav-file
    audio = audio.squeeze()
    audio = audio * 32768.0
    audio = audio.cpu().numpy().astype("int16")
    output_file = "output.wav"

    # Write audio file to disk
    # 22,05 kHz sample rate
    write(output_file, 22050, audio)

    # Play audio file
    # AudioPlayer(output_file).play(block=True)

    if "winsound" in mod:
        winsound.PlaySound(output_file, winsound.SND_FILENAME)
    else:
        # macOS
        # call(["afplay", "./output.wav"])
        # Linux
        call(["aplay", "./output.wav"])


"""
while 1:
    text = input("Input: ")

    # Tokenize, clean and phonemize input text
    x = prepare_text(text).to("cpu")

    with torch.no_grad():

        # Generate generic TTS-output
        old_time = time.time()
        tts_output = glados.generate_jit(x)
        print("Forward Tacotron took " + str((time.time() - old_time) * 1000) + "ms")

        # Use HiFiGAN as vocoder to make output sound like GLaDOS
        old_time = time.time()
        mel = tts_output["mel_post"].to(device)
        audio = vocoder(mel)
        print("HiFiGAN took " + str((time.time() - old_time) * 1000) + "ms")

        # Normalize audio to fit in wav-file
        audio = audio.squeeze()
        audio = audio * 32768.0
        audio = audio.cpu().numpy().astype("int16")
        output_file = "output.wav"

        # Write audio file to disk
        # 22,05 kHz sample rate
        write(output_file, 22050, audio)

        # Play audio file
        if "winsound" in mod:
            winsound.PlaySound(output_file, winsound.SND_FILENAME)
        else:
            call(["aplay", "./output.wav"])
"""
if __name__ == "__main__":
    glados_speak("Hello, I am GLaDOS. How are you doing today?")

if __name__ == "__main__":
    glados_speak("Katherine Chan")