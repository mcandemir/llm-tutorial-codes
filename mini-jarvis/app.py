import os
import dotenv

dotenv.load_dotenv()
from openai import OpenAI
from playsound import playsound
import warnings

# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


client = OpenAI(api_key=os.environ["OPENAI_KEY"])


def generate_audio(text):
    speech_file_path = "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(speech_file_path)
    playsound("speech.mp3")
    os.remove("speech.mp3")


def generate_completion(query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a friendly assistant that speaks like a normal human. Try to give short answers instead of long and detailed ones.",
            },
            {"role": "user", "content": query},
        ],
        max_tokens=64,
    )

    text = response.choices[0].message.content

    return text


if __name__ == "__main__":

    while True:
        print("(User):  ", end="")
        user_input = input()

        generated_text = generate_completion(user_input)
        print(f"(Assistant): {generated_text}")
        generate_audio(generated_text)
