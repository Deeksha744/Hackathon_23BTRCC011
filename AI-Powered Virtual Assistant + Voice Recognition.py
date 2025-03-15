import speech_recognition as sr
import pyttsx3
import datetime
smart_home = {
    "lights": "off",
    "temperature": 22,
    "alarm": "off"
}
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Capture voice input and convert to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
        except sr.RequestError:
            speak("Speech service is not available.")
    return None

def control_smart_home(command):
    """Process smart home commands and update states"""
    global smart_home

    if "turn on the lights" in command:
        smart_home["lights"] = "on"
        speak("Lights are now on.")

    elif "turn off the lights" in command:
        smart_home["lights"] = "off"
        speak("Lights are now off.")

    elif "set temperature to" in command:
        words = command.split()
        for word in words:
            if word.isdigit():
                smart_home["temperature"] = int(word)
                speak(f"Temperature is set to {word} degrees Celsius.")
                return
        speak("Please specify a valid temperature.")

    elif "check temperature" in command:
        speak(f"The current temperature is {smart_home['temperature']} degrees Celsius.")

    elif "set alarm for" in command:
        words = command.split()
        for word in words:
            if ":" in word:  
                smart_home["alarm"] = word
                speak(f"Alarm set for {word}.")
                return
        speak("Please provide a valid time.")

    elif "turn off alarm" in command:
        smart_home["alarm"] = "off"
        speak("Alarm is turned off.")

    elif "what time is it" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}")

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I didn't understand that command.")

if __name__ == "__main__":
    speak("Hello! How can I help you with your smart home?")
    while True:
        command = recognize_speech()
        if command:
            control_smart_home(command)
