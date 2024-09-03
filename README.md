# TheTypist2.0

TheTypist2.0 is an automated typing tool designed to simulate human typing in web-based typing tests or games. It consists of a Python backend using Flask and a frontend userscript for browser interaction. I previously tried to make this app in the past using C# and an OCR, but that did not work as intended so I tried again using the DOM and a flask server and it works perfect.

## Features

- Automated typing with adjustable WPM (Words Per Minute) and accuracy
- GUI for easy configuration of typing parameters
- Automatic race management
- reCAPTCHA handling
- Cross-platform support (Windows and macOS)

## Requirements

- Python 3.x
- PyQt5
- Flask
- Flask-CORS
- PyAutoGUI

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/andruwsorensen/TheTypist2.0.git
   cd TheTypist2.0
   ```

2. Install the required Python packages:
   ```
   pip install PyQt5 Flask Flask-CORS pyautogui
   ```

3. Install the userscript in your browser using a userscript manager like Tampermonkey.

## Usage

1. Run the Python backend:
   ```
   python app.py
   ```

2. The GUI will appear, allowing you to configure typing parameters.

3. Navigate to the typing website in your browser. The userscript will automatically interact with the page and communicate with the backend.

## Configuration

You can adjust the following parameters in the GUI:

- Time Between Race (seconds)
- Race Count
- WPM (Words Per Minute)
- Accuracy (%)

## How it works

The system consists of two main components:

1. Python Backend (app.py):
   - Handles the typing logic and automation
   - Provides a GUI for configuration
   - Runs a Flask server to communicate with the frontend

2. JavaScript Frontend (userscript):
   - Interacts with the webpage
   - Extracts text to be typed
   - Sends requests to the backend for typing and other actions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with the terms of service of any websites you interact with.
