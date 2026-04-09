import warnings
warnings.filterwarnings("ignore", message="All support for the `google.generativeai` package has ended")

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMInterface:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                tools=self.define_tools()
            )
            self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        else:
            self.model = None
            self.chat = None
        self.conversation_history = []

    def define_tools(self):
        """Define the tools for Gemini."""
        import pyautogui
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from bs4 import BeautifulSoup
        import requests

        def click_coordinate(x: int, y: int):
            """Moves the mouse to x, y and clicks. Use this to interact with desktop apps."""
            pyautogui.click(x, y)
            return f"Successfully clicked at {x}, {y}"

        def navigate_to_url(url: str):
            """Navigate to a specific URL in the browser."""
            # Note: This is simplified; in real implementation, manage browser instance
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)
            return f"Navigated to {url}"

        def scrape_text(url: str):
            """Scrape text content from a webpage."""
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()
                return text[:1000] + "..." if len(text) > 1000 else text
            except Exception as e:
                return f"Error scraping: {e}"

        return [click_coordinate, navigate_to_url, scrape_text]

    def reason(self, user_input, tools=None):
        """Send user input to LLM with tools and get response."""
        if not self.chat:
            return "Gemini API key not set. Please add GEMINI_API_KEY to .env file."
        
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"Error: {e}"