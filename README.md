# Jarvis
AI-Driven Personal Assistant (Project JARVIS).

## Revised Project Description: J.A.R.V.I.S. (Gemini Edition)

### Project Overview
J.A.R.V.I.S. is an AI-driven automation framework that leverages the Google Gemini 1.5 Pro/Flash API to create a multimodal personal assistant. Unlike standard chatbots, this system uses Gemini's sophisticated reasoning to interact with the local operating system and the web. By treating Python functions as "tools," Gemini can autonomously decide when to scrape a website with BeautifulSoup, automate a browser with Selenium, or control the desktop interface via PyAutoGUI.

### Technical Stack (Updated)
- **Core LLM**: Google Gemini API (gemini-1.5-flash for speed or 1.5-pro for complex reasoning).
- **Automation Suite**: PyAutoGUI (Desktop), Selenium (Web Browser), BeautifulSoup4 (Data Extraction).
- **Environment**: Python 3.10+, python-dotenv for secure API key management.

### Key Feature: Multimodal Reasoning
The ability to send screenshots of your desktop to Gemini so it can "see" what it needs to click.

### Technical Implementation: Connecting Gemini to your Tools
To get started, you'll need to install the library:
```
pip install -q -U google-generativeai
```

1. **The "Tool" Definition**
You must define your automation functions so Gemini knows how to use them.

```python
import google.generativeai as genai
import pyautogui
import os

# Define a tool for Jarvis to use
def click_coordinate(x: int, y: int):
    """Moves the mouse to x, y and clicks. Use this to interact with desktop apps."""
    pyautogui.click(x, y)
    return f"Successfully clicked at {x}, {y}"

# Initialize Gemini with your API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Create the model and 'attach' the tools
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[click_coordinate] # Add your Selenium/BS4 functions here too
)
```

2. **The Execution Loop**
When you give a command, Gemini will return a "Function Call" instead of just text if it thinks it needs to move the mouse.

```python
# Start a chat session with automatic function calling
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message("Jarvis, click the center of my screen.")
print(response.text)
```

### Why Gemini for a Jarvis project?
- **Massive Context**: You can feed Jarvis entire PDF manuals or long code files, and it won't "forget" the beginning of the conversation.
- **Native Video/Image Support**: Since you're using PyAutoGUI, you can take a screenshot with pyautogui.screenshot(), send it to Gemini, and ask: "Where is the 'Submit' button in this image?" Gemini will give you the (x, y) coordinates to click.
- **Cost-Efficiency**: The gemini-1.5-flash model is incredibly fast and offers a generous free tier for developers.

### Pro-Tip
Make sure to store your API key in a .env file and never hardcode it. Since you're working on a project with Erneste and Bruce, using environment variables ensures you don't accidentally share your private key when swapping code!
