import speech_recognition as sr
from gtts import gTTS
import playsound
import webbrowser
import google.generativeai as genai
import re
from google.generativeai import GenerativeModel
from pytube import Search
import os
from newsapi import NewsApiClient
import requests


url = "https://newsapi.org/v2/top-headlines"
api_key = "70dac97425304aa0958595a11abab63a"
params = {
    'country': 'in',
    'apiKey': api_key
}

def search_and_play_youtube(query):
    search = Search(query)
    results = search.results

    if results:
        video_url = results[0].watch_url
        webbrowser.open(video_url)
        speak(f"Playing: {results[0].title}")
    else:
        speak("No results found.")

def clean_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text

recognizer = sr.Recognizer()

def speak(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def speak_with_gemini(prompt, max_words=40):
    max_tokens = int(max_words * 0.75)
    genai.configure(api_key="AIzaSyC9RvYFdAk_HuTYdQVbrDZFKiYonwcYHc8")
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    cleaned_text = clean_text(response.text)
    words = cleaned_text.split()
    limited_text = ' '.join(words[:max_words])
    speak(limited_text)
    print(limited_text)

def process_command(command):
    if "open" in command:
        website = command.replace("open", "").strip()
        webbrowser.open(f"https://{website}.com")
        speak(f"Opening {website}")
    elif "play" in command:
        song = command.replace("play", "").strip()
        search_and_play_youtube(song)
        speak(f"Playing {song}")
    elif "news" in command.lower():
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for article in data['articles']:
                speak(article['title'])
    else:
        speak_with_gemini(command, max_words=40)

if __name__ == "__main__":
    speak("Initializing Aahana", lang='hi')

    while True:
        print("Recognizing")
        try:
            with sr.Microphone() as source:
                print("Say Something!")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=1)
                word = recognizer.recognize_google(audio)

            if word.lower() == "suno":
                speak("Ji kahiye", lang='hi')
                with sr.Microphone() as source:
                    print("Aahana Active!")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    command = recognizer.recognize_google(audio)
                    process_command(command)
                    print(command)
        except Exception as e:
            print(f"Listening Error; {e}")
