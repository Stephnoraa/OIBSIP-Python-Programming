import requests
import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage
import wikipedia
import logging
from datetime import datetime
import pywhatkit
import os

# Setting up logging
logging.basicConfig(filename='voice_assistant_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

USER = os.getenv('USER')  # Fetching the USER environment variable
EMAIL = os.getenv('EMAIL')  # Fetching the EMAIL environment variable
PASSWORD = os.getenv('PASSWORD')  # Fetching the PASSWORD environment variable
OPENWEATHER_APP_ID = os.getenv('OPENWEATHER_APP_ID')

# Initialize the text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet():
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    speak(f"{greeting}, {USER}. How can I assist you today?")


def command():
    with sr.Microphone() as source:
        print("Clearing background noises... Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Ask me anything...")
        audio = recognizer.listen(source)

    try:
        cmd = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {cmd}")
        return cmd.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        logging.error("Error: Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        logging.error(f"Error in recognizing audio: {e}")
    except Exception as e:
        print("An error occurred.")
        logging.error(f"Unexpected error: {e}")
    return ""


def get_weather_report(city):
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric")
        data = response.json()
        if data.get("cod") != 200:
            return f"Error: {data.get('message', 'Unable to fetch weather data.')}"
<<<<<<< HEAD

=======
        
>>>>>>> ad5e0ac45f9791f328cdaadf9c9c8e015681e8b2
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather in {city} is currently {weather} with a temperature of {temperature}°C."
    except requests.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return "Error fetching weather data."


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

        elif "play" in cmd:
            video = cmd.split("play")[-1].strip()
            pywhatkit.playonyt(video)

        elif "exit" in cmd:
            speak("Goodbye, have a nice day!")
            break

        else:
            speak("Sorry, I don't understand that command.")


if __name__ == "__main__":
    main()