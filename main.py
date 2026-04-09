#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System (Gemini Edition)
Main entry point for the AI assistant.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from jarvis.voice import VoiceInterface
from jarvis.llm import LLMInterface
from jarvis.automation import AutomationTools

def main():
    voice = VoiceInterface(use_voice=False)  # Set to True for voice mode
    llm = LLMInterface()
    automation = AutomationTools()

    print("J.A.R.V.I.S. (Gemini Edition) is ready. Press Enter to start.")

    while True:
        if voice.listen_for_wake_word():
            voice.text_to_speech("Yes, sir?")
            user_input = voice.speech_to_text()
            if user_input:
                response = llm.reason(user_input)
                voice.text_to_speech(response)

if __name__ == "__main__":
    main()