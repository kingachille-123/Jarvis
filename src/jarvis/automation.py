import pyautogui
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os
from PIL import Image

class AutomationTools:
    def __init__(self):
        self.driver = None

    def start_browser(self):
        """Start Chrome browser."""
        if not self.driver:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return "Browser started."

    def navigate_to_url(self, url):
        """Navigate to a URL."""
        if self.driver:
            self.driver.get(url)
            return f"Navigated to {url}."
        return "Browser not started."

    def click_element(self, selector):
        """Click an element by CSS selector."""
        if self.driver:
            try:
                element = self.driver.find_element("css_selector", selector)
                element.click()
                return "Element clicked."
            except Exception as e:
                return f"Error clicking element: {e}"
        return "Browser not started."

    def click_coordinate(self, x: int, y: int):
        """Moves the mouse to x, y and clicks. Use this to interact with desktop apps."""
        pyautogui.click(x, y)
        return f"Successfully clicked at {x}, {y}"

    def type_text(self, text, selector=None):
        """Type text, optionally into an element."""
        if selector and self.driver:
            try:
                element = self.driver.find_element("css_selector", selector)
                element.send_keys(text)
                return "Text typed."
            except Exception as e:
                return f"Error typing: {e}"
        else:
            pyautogui.typewrite(text)
            return "Text typed on screen."

    def scroll_down(self, amount=500):
        """Scroll down the page."""
        if self.driver:
            self.driver.execute_script(f"window.scrollBy(0, {amount});")
            return "Scrolled down."
        else:
            pyautogui.scroll(-amount)
            return "Scrolled down."

    def take_screenshot(self, filename="screenshot.png"):
        """Take a screenshot."""
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"Screenshot saved as {filename}."

    def get_screenshot_image(self):
        """Take a screenshot and return PIL Image."""
        return pyautogui.screenshot()

    def scrape_text(self, url):
        """Scrape text from a webpage."""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            return text[:1000] + "..." if len(text) > 1000 else text
        except Exception as e:
            return f"Error scraping: {e}"

    def close_browser(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            return "Browser closed."