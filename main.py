import random
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyaudio
import requests
import subprocess
import cv2
import ctypes
from bs4 import BeautifulSoup
from googlesearch import search
from PyDictionary import PyDictionary

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def set_brightness(brightness):
    # Convert brightness value (0-100) to the range (0-255)
    brightness_value = int(brightness * 255 / 100)

    # Call the SetDeviceGammaRamp function from the Windows API
    ctypes.windll.user32.SetDeviceGammaRamp(0, ctypes.c_void_p(brightness_value), 0)


def start_emotion_detection():
    # Replace 'python emotion_detection_project.py' with the command to start your emotion detection project
    subprocess.Popen(["python", "emotion_detection_project.py"])


def stop_emotion_detection():
    # Terminate the process associated with the emotion detection project
    subprocess.run(["pkill", "-f", "emotion_detection_project.py"])


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Alexa Two Point o Sir. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"

    return query.lower()


def capture_photo():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        speak("Error: Unable to open camera.")
        return

    speak("Smile! Capturing photo...")

    # Capture a single frame from the camera
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        speak("Error: Unable to capture photo.")
        return

    # Save the captured frame as a JPEG image
    filename = "captured_photo.jpg"
    cv2.imwrite(filename, frame)

    speak("Photo captured successfully!")

    # Release the camera
    cap.release()


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("youremail@gmail.com", "your-password")
    server.sendmail("youremail@gmail.com", to, content)
    server.close()


def search_web(query):
    try:
        for j in search(query, num=1, stop=1, pause=2):
            webbrowser.open(j)
    except Exception as e:
        print(e)
        speak("Sorry, I encountered an error while searching the web.")


def search_website(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("a")

        for result in search_results:
            url = result.get("href")
            if "url?q=" in url and "webcache" not in url:
                url = url.split("?q=")[1].split("&sa=U")[0]
                webbrowser.open(url)
                return
        print("Sorry, couldn't find relevant website.")
    except Exception as e:
        print("Error:", e)

def remind_user():
    speak("What would you like me to remind you?")
    reminder = takeCommand()
    speak("When should I remind you?")
    time = takeCommand()
    # Implement reminder logic here


def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
    ]
    joke = random.choice(jokes)
    speak(joke)


def set_volume(volume_level):
    try:
        volume = int(volume_level)
        engine.setProperty(
            "volume", volume / 100
        )  # Volume should be set between 0 and 1
        speak(f"Volume set to {volume_level}%")
    except ValueError:
        speak("Please provide a valid volume level.")


def set_alarm():
    speak("What time should I set the alarm for?")
    alarm_time = takeCommand()

    # Parse the user-provided time
    alarm_time = alarm_time.lower()
    if "hour" in alarm_time and "minute" in alarm_time:
        try:
            hour = int(alarm_time.split("hour")[1].split("minute")[0].strip())
            minute = int(alarm_time.split("minute")[1].strip())
            alarm_time = datetime.time(hour=hour, minute=minute)
            print(alarm_time)
            current_time = datetime.datetime.now().time()

            # Calculate the time difference
            delta_hours = alarm_time.hour - current_time.hour
            delta_minutes = alarm_time.minute - current_time.minute
            delta_seconds = (delta_hours * 3600) + (delta_minutes * 60)

            if delta_seconds > 0:
                speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")
                # Wait until the alarm time
                time.sleep(delta_seconds)
                # Trigger the alarm
                speak("Alarm!")
            else:
                speak("Please provide a valid time in the future.")
        except Exception as e:
            print("Error:", e)
            speak("Sorry, I couldn't set the alarm.")
    else:
        speak("Please provide a valid time including hour and minute.")


def get_word_meaning(word):
    dictionary = PyDictionary()
    meaning = dictionary.meaning(word)
    if meaning:
        speak(f"The meaning of {word} is {meaning['Noun'][0]}")
    else:
        speak(f"Sorry, I couldn't find the meaning of {word}")


def get_word_synonyms(word):
    dictionary = PyDictionary()
    synonyms = dictionary.synonym(word)
    if synonyms:
        speak(f"The synonyms of {word} are {', '.join(synonyms)}")
    else:
        speak(f"Sorry, I couldn't find synonyms for {word}")


def get_word_antonyms(word):
    dictionary = PyDictionary()
    antonyms = dictionary.antonym(word)
    if antonyms:
        speak(f"The antonyms of {word} are {', '.join(antonyms)}")
    else:
        speak(f"Sorry, I couldn't find antonyms for {word}")


def pronounce_word(word):
    speak(f"The pronunciation of {word} is {word}")


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif "capture photo" in query:
            capture_photo()

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            speak("What would you like to search on Google?")
            search_query = takeCommand()
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            speak(f"Searching Google for {search_query}")

            # Make a request to the Google search page
            google_page = requests.get(search_url)
            soup = BeautifulSoup(google_page.content, "html.parser")

            # Find and extract the first search result
            search_results = soup.find_all("div", class_="tF2Cxc")
            if search_results:
                first_result = (
                    search_results[0].find("div", class_="BNeawe iBp4i AP7Wnd").text
                )
                speak("Here is the first result from Google:")
                speak(first_result)
            else:
                speak("Sorry, I couldn't find any search results.")

        elif "open stackoverflow" in query:
            webbrowser.open("stackoverflow.com")

        elif "open website" in query:
            speak("Which website would you like to open?")
            website_query = takeCommand()
            search_website(website_query)
        elif "play music" in query:
            music_dir = "D:\\Non Critical\\songs\\Favorite Songs2"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "open code" in query:
            codePath = "D:\\VSCode\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif "open word" in query:
            codePath1 = (
                r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
            )
            os.startfile(codePath1)

        elif "email to saksham" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "sakshamEmail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend Saksham Bro. I am not able to send this email")

        elif "epoxy" in query:
            query = query.replace("chatgpt", "")
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": query}],
                    model="gpt-3.5-turbo",
                )
                chat_response = chat_completion.choices[0].message["content"]
                speak(chat_response)
                print(chat_response)
            except Exception as e:
                print("Error:", e)
                speak("Sorry, I encountered an error while processing your request.")

        elif "search" in query:
            search_query = query.replace("search", "")
            speak(f"Searching the web for {search_query}")
            search_web(search_query)

        elif "weather" in query:
            get_weather()

        elif "reminder" in query:
            remind_user()

        elif "joke" in query:
            tell_joke()

        elif "volume" in query:
            query_split = query.split()
            volume_level = query_split[query_split.index("volume") + 1]
            set_volume(volume_level)

        elif "set alarm" in query:
            set_alarm()

        elif "meaning" in query:
            word = query.split("meaning")[1].strip()
            get_word_meaning(word)

        elif "synonyms" in query:
            word = query.split("synonyms")[1].strip()
            get_word_synonyms(word)

        elif "antonyms" in query:
            word = query.split("antonyms")[1].strip()
            get_word_antonyms(word)

        elif "pronounce" in query:
            word = query.split("pronounce")[1].strip()
            pronounce_word(word)

        elif "set brightness to" in query:
            try:
                brightness_level = int(query.split("to")[1].strip())
                if 0 <= brightness_level <= 100:
                    set_brightness(brightness_level)
                    speak(f"Brightness set to {brightness_level} percent.")
                else:
                    speak("Please provide a brightness level between 0 and 100.")
            except ValueError:
                speak("Please provide a valid brightness level.")
