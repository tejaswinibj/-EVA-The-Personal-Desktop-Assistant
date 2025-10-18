import speech_recognition
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

# Optional: to help identify input devices if needed
import sounddevice as sd
print("Available Input Devices:")
print(sd.query_devices())

def takeCommand():
    r = speech_recognition.Recognizer()
    
    # OPTIONAL: Set specific mic device index if default doesn't work
    # Replace 1 with the correct device index after checking the list
    with speech_recognition.Microphone(device_index=None) as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

query = takeCommand().lower()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("eva", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)

        except:
            speak("No speakable output available")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("eva", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from wikipedia....")
        query = query.replace("wikipedia", "")
        query = query.replace("search wikipedia", "")
        query = query.replace("eva", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia..")
        print(results)
        speak(results)
