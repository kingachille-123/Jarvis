import pyttsx3
import os
from dotenv import load_dotenv

try:
    from elevenlabs import generate, play
    elevenlabs_available = True
except ImportError:
    elevenlabs_available = False

load_dotenv()

class VoiceInterface:
    def __init__(self, use_voice=True):
        # For STT, we can use a different service or keep text for now
        # Gemini doesn't have built-in STT, so placeholder
        self.tts_engine = pyttsx3.init()
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.wake_word = os.getenv('WAKE_WORD', 'jarvis').lower()
        self.use_voice = use_voice

    def listen_for_wake_word(self):
        """Listen for wake word or simulate."""
        if self.use_voice:
            # Placeholder for wake word detection
            return True
        else:
            input("Press Enter to start listening...")
            return True

    def speech_to_text(self):
        """Capture audio and convert to text or use text input."""
        if self.use_voice:
            # For now, simulate with text input
            return input("Enter your command: ")
        else:
            return input("Enter your command: ")

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