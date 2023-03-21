import torch
from utils.tools import prepare_text
from scipy.io.wavfile import write
from sys import modules as mod
import os
from playsound import playsound
from time import sleep


try:
    import winsound

    # set espeak os environment variable
    os.environ[
        "PHONEMIZER_ESPEAK_LIBRARY"
    ] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
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
glados_path = os.path.join(os.path.dirname(__file__), "models", "glados.pt")
glados = torch.jit.load(glados_path, map_location=device)
vocoder_path = os.path.join(os.path.dirname(__file__), "models", "vocoder-gpu.pt")
vocoder = torch.jit.load(vocoder_path, map_location=device)

# Prepare models in RAM
for i in range(4):
    init = glados.generate_jit(prepare_text(str(i)))
    init_mel = init["mel_post"].to(device)
    init_vo = vocoder(init_mel)


def glados_speak(
    text: str, output_file: str = "output.wav", silenced: bool = False
) -> None:
    """
    generates audio from text and plays it
    silenced mode is generally only used for debug purposes as it skips the entire audio generation process
    """
    if silenced:
        print("Silenced, skipping audio generation and only printing text")
        print(text)
        return
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

    # Write audio file to disk
    # 22,05 kHz sample rate
    write(output_file, 22050, audio)

    try:
        call(["aplay", output_file])
    except:
        playsound(output_file, block=False)


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
    glados_speak("Baking cakes.")
