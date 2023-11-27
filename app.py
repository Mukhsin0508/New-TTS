import os
from google.cloud import texttospeech
from google.cloud.texttospeech import SynthesisInput, VoiceSelectionParams, AudioConfig, AudioEncoding

# Set the path to your service account key
key_path = "/Users/mukhsinmukhtorov/Desktop/TTS/.env"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# Set the path to the user_input file
user_input_file = "user_input.txt"

# Read the text from the user_input file
with open(user_input_file, "r") as file:
    user_input_text = file.read()

# Set the text input to be synthesized
synthesis_input = SynthesisInput(text=user_input_text)

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Define default voice types
voice1 = VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Neural2-C"
)
voice2 = VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Neural2-F"
)
voice3 = VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Neural2-I"
)

# Create a list of voices for easier management
my_voice_list = [voice1, voice2, voice3]

# Use one of the predefined voices directly
def choose_voice():
    while True:
        for idx, voice in enumerate(my_voice_list, start=1):
            print(f"{idx}. {voice.name}")
        selected_idx = input("Choose a voice (enter the number): ")
        try:
            selected_idx = int(selected_idx) - 1
            if 0 <= selected_idx < len(my_voice_list):
                selected_voice = my_voice_list[selected_idx]
                print(f"You've selected the voice: {selected_voice.name}")
                return selected_voice
            else:
                print("Invalid voice selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

selected_voice = choose_voice()

# Use the selected voice in the TTS operation
audio_config = AudioConfig(
    audio_encoding=AudioEncoding.LINEAR16,
    effects_profile_id=["small-bluetooth-speaker-class-device"],
    pitch=1,
    speaking_rate=0.90
)

try:
    response = client.synthesize_speech(
        input=synthesis_input, voice=selected_voice, audio_config=audio_config
    )
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
except Exception as e:
    print(f"Error occurred: {e}")
