import os
import random
import logging
import datetime
import requests
import smtplib
import speech_recognition as sr
import pyttsx3
import subprocess
from email.message import EmailMessage
import wikipedia
import pywhatkit
import pyjokes
import pyaudio
import pyautogui

# Setting up logging
logging.basicConfig(filename='voice_assistant_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

USER = os.getenv('USER')  # Fetching the USER environment variable
EMAIL = os.getenv('EMAIL')  # Fetching the EMAIL environment variable
PASSWORD = os.getenv('PASSWORD')  # Fetching the PASSWORD environment variable
OPENWEATHER_APP_ID = os.getenv('OPENWEATHER_APP_ID')  # Fetching the OPENWEATHER_APP_ID environment variable

print(f"User: {USER}")
print(f"Email: {EMAIL}")


# Initialize the text-to-speech engine and speech recognizer
engine = pyttsx3.init()
recognizer = sr.Recognizer()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    speak(f"{greeting}, {USER}. How can I assist you today?")

def command():
    with sr.Microphone() as source:
        print("Clearing background noises... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            cmd = recognizer.recognize_google(audio, language="en-US")
            print(f"You said: {cmd}")
            return cmd.lower()
        except Exception as e:
            print("Sorry, I could not understand the audio.")
            logging.error(f"Error in recognizing audio: {e}")
            return ""

def get_weather_report(city):
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric")
    data = response.json()
    if data.get("cod") != 200:
        return f"Error: {data.get('message', 'Unable to fetch weather data.')}"

    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    return f"The weather in {city} is currently {weather} with a temperature of {temperature}°C."

def send_email(receiver_address, subject, message):
    email = EmailMessage()
    email['To'] = receiver_address
    email['Subject'] = subject
    email['From'] = EMAIL
    email.set_content(message)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(email)
        speak("Email sent.")

def screenshot():
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

# def play_music(song_name=None):
#     song_dir = os.path.expanduser("~\\Music")
#     songs = os.listdir(song_dir)
#
#     if song_name:
#         songs = [song for song in songs if song_name.lower() in song.lower()]
#
#     if songs:
#         song = random.choice(songs)
#         os.startfile(os.path.join(song_dir, song))
#         speak(f"Playing {song}.")
#         print(f"Playing {song}.")
#     else:
#         speak("No song found.")
#         print("No song found.")




def play_music(song_name=None):
    # This is a placeholder dictionary. You will need to fill it with actual song names and their URIs.
    song_uris = {
        "song1": "spotify:track:https://open.spotify.com/track/5sPJPiDr73PgyVvhjiLvQQ?si=pHLi7fNIQNev9svf6D9udw",
        "song2": "spotify:track:https://open.spotify.com/track/2e3Ea0o24lReQFR4FA7yXH?si=cjmRiVHuSGaVp8FbPPFAtw&context=spotify%3Asearch%3Alove%2B",
        "song3": "spotify:track:https://open.spotify.com/track/59nOXPmaKlBfGMDeOVGrIK?si=c3kB6t2cSM6eS_drQ2L9XA&context=spotify%3Asearch%3Alove%2B",
        "song4": "spotify:track:https://open.spotify.com/track/1MIGkQxcdAt2lDx6ySpsc5?si=NYHBfLb1TNSrLznNRsHcXw",
        # Add more songs as needed
    }

    # Convert song_name to lowercase for case-insensitive search
    if song_name:
        song_name_lower = song_name.lower()
        matching_songs = {name: uri for name, uri in song_uris.items() if song_name_lower in name.lower()}

        if matching_songs:
            selected_song = random.choice(list(matching_songs.items()))
            uri_to_play = selected_song[1]
            # Open Spotify with the song URI
            subprocess.Popen(['spotify:', uri_to_play])
            speak(f"Playing {selected_song[0]} on Spotify.")
            print(f"Playing {selected_song[0]} on Spotify.")
        else:
            speak("No song found.")
            print("No song found.")
    else:
        speak("Please provide a song name.")
        print("Please provide a song name.")


def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

def main():
    greet()

    while True:
        cmd = command()

        if "weather" in cmd:
            city = cmd.split("in")[-1].strip()
            weather_report = get_weather_report(city)
            speak(weather_report)

        elif "email" in cmd:
            speak("Who do you want to send the email to?")
            receiver = command()
            speak("What is the subject?")
            subject = command()
            speak("What is the message?")
            message = command()
            send_email(receiver, subject, message)

        elif "time" in cmd:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            speak("The current time is " + current_time)
            print("The current time is", current_time)

        elif "date" in cmd:
            now = datetime.datetime.now()
            speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}")
            print(f"The current date is {now.day}/{now.month}/{now.year}")

        elif "wikipedia" in cmd:
            query = cmd.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in cmd:
            song_name = cmd.replace("play music", "").strip()
            play_music(song_name)

        elif "screenshot" in cmd:
            screenshot()

        elif "tell me a joke" in cmd:
            tell_joke()

        elif "shutdown" in cmd:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break

        elif "restart" in cmd:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break

        elif "offline" in cmd or "exit" in cmd:
            speak("Going offline. Have a good day!")
            break

        else:
            speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
