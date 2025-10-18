import requests
import json
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def latestnews():
    api_dict = {
        "business" : "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=54d9529f2af84a3696f3c00016dd922b",
        "entertainment" : "https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=54d9529f2af84a3696f3c00016dd922b",
        "health" : "https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=54d9529f2af84a3696f3c00016dd922b",
        "science" :"https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey=54d9529f2af84a3696f3c00016dd922b",
        "sports" :"https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=54d9529f2af84a3696f3c00016dd922b",
        "technology" :"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=54d9529f2af84a3696f3c00016dd922b"
    }
    content = None
    url = None
    speak("Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
    field = input("Type field news that you want: ")
    for key ,value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was found")
            break
        else:
            url = True
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts :
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")

        a = input("[press 1 to cont] and [press 2 to stop]")
        if str(a) == "1":
            pass
        elif str(a) == "2":
            break

    speak("thats all")
