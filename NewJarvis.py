import speech_recognition as sr
import pyttsx3
import webbrowser
from google.generativeai import GenerativeModel
import music

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


    elif "what is the meaning of life" in command.lower():
        speak_with_gemini(command)
    else:
        speak("Command not recognized")

def speak_with_gemini(prompt):
    # Use your actual API key here
    api_key = "AIzaSyC9RvYFdAk_HuTYdQVbrDZFKiYonwcYHc8"
    
    # Initialize the model with the API key
    model = GenerativeModel(api_key=api_key)
    
    try:
        response = model.generate_content(prompt)
        speak(response["text"])
    except Exception as e:
        speak("Sorry, I could not get a response.")
        print(f"Error using GenerativeModel: {e}")

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("Initializing Deadpool")
    
    while True:
        print("Listening for the wake word 'Deadpool'...")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio).lower()
                
            if word == "deadpool":
                speak("Yes! How may I help you, Sir?")
                with sr.Microphone() as source:
                    print("Deadpool Active!")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    process_command(command)
        except Exception as e:
            print(f"Listening Error: {e}")
