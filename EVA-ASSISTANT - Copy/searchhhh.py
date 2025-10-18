import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("voice", engine.getProperty("voices")[1].id)
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_recognize(duration=4, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Processing...")

    recognizer = sr.Recognizer()
    try:
        audio_data = sr.AudioData(audio.tobytes(), fs, 2)
        text = recognizer.recognize_google(audio_data, language='en-in')
        print(f"You said: {text}")
        speak(f"You said: {text}")
        return text.lower()
    except Exception as e:
        print("Sorry, could not understand.")
        speak("Sorry, I could not understand what you said.")
        return "none"

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("google search", "").replace("google", "").strip()
        speak("This is what I found on Google")
        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)
        except:
            speak("No speakable output available or couldn't fetch summary.")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "").replace("youtube", "").strip()
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done!")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from Wikipedia....")
        query = query.replace("wikipedia", "").replace("search wikipedia", "").strip()

        if not query:
            speak("Sorry, I didn't catch what you want to search on Wikipedia.")
            return

        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia..")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results for your query. Please be more specific.")
            print("Options:", e.options)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any page with that title.")
        except Exception as e:
            speak("An error occurred while searching Wikipedia.")
            print(e)

# --- MAIN FLOW ---
query = listen_and_recognize()

if query != "none":
    if "google" in query:
        searchGoogle(query)
    elif "youtube" in query:
        searchYoutube(query)
    elif "wikipedia" in query:
        searchWikipedia(query)
    else:
        speak("I can search Google, YouTube, or Wikipedia. Please mention one of them.")
else:
    speak("Please try again.")
