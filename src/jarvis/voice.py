import pyttsx3
import os
from dotenv import load_dotenv

try:
    from elevenlabs import generate, play
    elevenlabs_available = True
except ImportError:
    elevenlabs_available = False

try:
    import speech_recognition as sr
    speech_available = True
except ImportError:
    speech_available = False

try:
    import pyaudio
    pyaudio_available = True
except ImportError:
    pyaudio_available = False

speech_available = speech_available and pyaudio_available

load_dotenv()

class VoiceInterface:
    def __init__(self, use_voice=True):
        self.tts_engine = pyttsx3.init()
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.wake_word = os.getenv('WAKE_WORD', 'jarvis').lower()
        self.use_voice = use_voice and speech_available
        if speech_available:
            self.recognizer = sr.Recognizer()
        if not speech_available and use_voice:
            print("Speech recognition not available. Falling back to text input.")

    def listen_for_wake_word(self):
        """Listen for wake word."""
        if not self.use_voice:
            input("Press Enter to start listening...")
            return True
        with sr.Microphone() as source:
            print("Listening for wake word...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio).lower()
                if self.wake_word in text:
                    return True
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
        return False

    def speech_to_text(self):
        """Capture audio and convert to text."""
        if not self.use_voice:
            return input("Enter your command: ")
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""

    def text_to_speech(self, text):
        """Convert text to speech."""
        print(f"JARVIS: {text}")
        if self.elevenlabs_api_key and elevenlabs_available:
            try:
                audio = generate(text=text, api_key=self.elevenlabs_api_key)
                play(audio)
            except Exception as e:
                print(f"ElevenLabs error: {e}")
                self.fallback_tts(text)
        else:
            self.fallback_tts(text)

    def fallback_tts(self, text):
        """Fallback TTS using pyttsx3."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()