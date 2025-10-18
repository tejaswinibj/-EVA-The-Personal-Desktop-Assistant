import time
import datetime
import pyttsx3
import requests
from bs4 import BeautifulSoup
import os
import pyautogui
import random
import webbrowser
from plyer import notification
from pygame import mixer
import speedtest as speedtest_cli
import sounddevice as sd
import numpy as np
import speech_recognition as sr

# Password check and intro GIF
for i in range(3):
    a = input("Enter Password to open eva:- ")
    with open("password.txt", "r") as pw_file:
        pw = pw_file.read().strip()
    if a == pw:
        print("WELCOME! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        from INTRO import play_gif
        play_gif()  # Only once
        break
    elif i == 2:
        exit()
    else:
        print("Try Again")

# Text-to-Speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    recognizer = sr.Recognizer()
    fs = 44100
    duration = 4
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Processing...")
    try:
        audio_data = sr.AudioData(audio.tobytes(), fs, 2)
        query = recognizer.recognize_google(audio_data, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()
    except Exception:
        print("Say that again")
        return "None"

def alarm(query):
    alarm_time = query.split("and")
    alarm_hour = int(alarm_time[0].strip())
    alarm_minute = int(alarm_time[1].strip())
    alarm_second = int(alarm_time[2].strip())
    speak(f"Alarm is set for {alarm_hour}:{alarm_minute}:{alarm_second}")
    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_hour and now.minute == alarm_minute and now.second == alarm_second:
            speak("Alarm ringing...")
            mixer.init()
            mixer.music.load("alarm.wav")
            mixer.music.play()
            break
        time.sleep(1)

def schedule_day():
    speak("Do you want to clear old tasks? (Please speak YES or NO)")
    query = takeCommand()
    if "yes" in query:
        open("schedule.txt", "w").close()
        speak("Old tasks cleared.")
    no_tasks = int(input("Enter the number of tasks: "))
    for i in range(no_tasks):
        task = input(f"Enter task {i + 1}: ")
        with open("schedule.txt", "a") as file:
            file.write(f"{i + 1}. {task}\n")
    speak("Your tasks have been scheduled.")

def show_schedule():
    try:
        with open("schedule.txt", "r") as file:
            content = file.read().strip()
        if content:
            print(content)
            mixer.init()
            mixer.music.load("notification.mp3.wav")
            mixer.music.play()
            notification.notify(title="My Schedule", message=content, timeout=15)
            speak("I have shown your schedule in the notification.")
        else:
            speak("Your schedule is empty.")
    except FileNotFoundError:
        speak("No schedule found. Please schedule your day first.")

# --- Main Loop ---
if __name__ == "__main__":
    while True:
        query = takeCommand()

        if "wake up" in query:
            from newgreetme import greetMe
            greetMe()

            while True:
                query = takeCommand()

                if "go to sleep" in query:
                    speak("Okay, you can call me anytime.")
                    break

                elif "hello" in query:
                    speak("Hello, how are you?")
                    follow_up = takeCommand()
                    if "i am fine" in follow_up:
                        speak("That's great to hear!")
                    elif "how are you" in follow_up:
                        speak("I'm always good, thank you!")
                    elif "thank you" in follow_up:
                        speak("You're welcome.")

                elif "change password" in query:
                    speak("What's the new password?")
                    new_pw = input("Enter the new password: ")
                    with open("password.txt", "w") as f:
                        f.write(new_pw)
                    speak("Password updated successfully.")

                elif "schedule my day" in query:
                    schedule_day()

                elif "show my schedule" in query:
                    show_schedule()

                elif "open" in query:
                    query = query.replace("open", "").replace("eva", "")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")

                elif "internet speed" in query:
                    wifi = speedtest_cli.Speedtest()
                    upload_net = wifi.upload() / 1048576
                    download_net = wifi.download() / 1048576
                    speak(f"Download speed is {download_net:.2f} Mbps")
                    speak(f"Upload speed is {upload_net:.2f} Mbps")

                elif "play a game" in query:
                    from game import game_play
                    game_play()

                elif "screenshot" in query:
                    im = pyautogui.screenshot()
                    im.save("ss.jpg")

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("Smile!")
                    pyautogui.press("enter")

                elif "tired" in query:
                    speak("Playing your favourite songs.")
                    songs = [
                        "https://www.youtube.com/watch?v=jDErhADhhmg",
                        "https://www.youtube.com/watch?v=TjUXr560Gu0",
                        "https://www.youtube.com/watch?v=1wEtmB3z_yc"
                    ]
                    webbrowser.open(random.choice(songs))

                elif "pause" in query or "play" in query:
                    pyautogui.press("k")
                    speak("Toggled playback.")

                elif "mute" in query:
                    pyautogui.press("m")
                    speak("Muted.")

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Increasing volume.")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Decreasing volume.")
                    volumedown()

                elif "google" in query:
                    from searchhhh import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from searchhhh import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from searchhhh import searchWikipedia
                    searchWikipedia(query)

                elif "weather" in query or "temperature" in query:
                    try:
                        url = "https://www.google.com/search?q=temperature+in+bengaluru"
                        headers = {
                            "User-Agent": "Mozilla/5.0"
                        }
                        r = requests.get(url, headers=headers)
                        soup = BeautifulSoup(r.text, "html.parser")
                        temp = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
                        if temp:
                            temperature = temp.text
                            speak(f"Current temperature is {temperature}")
                        else:
                            speak("Could not retrieve the temperature.")
                    except Exception as e:
                        speak("Error fetching weather.")
                        print(e)

                elif "the time" in query:
                    now = datetime.datetime.now().strftime("%H:%M")
                    speak(f"The time is {now}")

                elif "finally sleep" in query:
                    speak("Going to sleep, sir.")
                    exit()

                elif "set an alarm" in query:
                    speak("Set the time like 7 and 30 and 0")
                    alarm_time = input("Enter alarm time: ")
                    alarm(alarm_time)

                elif "remember that" in query:
                    remember_msg = query.replace("remember that", "").strip()
                    with open("remem.txt", "a") as file:
                        file.write(remember_msg + "\n")
                    speak("I will remember that.")

                elif "what do you remember" in query:
                    try:
                        with open("remem.txt", "r") as file:
                            data = file.read().strip()
                            if data:
                                speak("You asked me to remember this:")
                                speak(data)
                            else:
                                speak("I don't remember anything yet.")
                    except FileNotFoundError:
                        speak("Memory file not found.")

                elif "shutdown system" in query:
                    speak("Are you sure you want to shut down?")
                    confirm = input("Shutdown the system? (yes/no): ")
                    if confirm.lower() == "yes":
                        os.system("shutdown /s /t 1")
