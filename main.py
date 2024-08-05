import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_recognize():
    try:
        with sr.Microphone() as source:
            print("Say Something!")
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            print(f"Recognized word: {word}")
            return word
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Listening Error: {e}")

if __name__ == "__main__":
    speak("Initializing Deadpool")

    while True:
        print("Waiting for the wake word 'Deadpool'...")
        word = listen_and_recognize()
        if word and word.lower() == "deadpool":
            speak("Yes")
            print("Deadpool Active!")
            command = listen_and_recognize()
            if command:
                print(f"Recognized command: {command}")
                # Process command here
