# TheTypist2.0

TheTypist2.0 is an automated typing tool designed to simulate human interaction with online typing games or tests, such as [nitrotype.com](https://www.nitrotype.com/). Its primary purpose is to automate race participation—enabling rapid, customizable typing speeds and accuracy for educational, experimental, or fun use cases.

## Technologies Used

- **Python 3.x**: The backend is built with Python and serves both as the logic engine and a GUI configuration panel.
- **Flask**: Provides a lightweight web server for communication between the browser userscript and Python logic.
- **Flask-CORS**: Handles cross-origin requests from the browser.
- **PyAutoGUI**: Controls keyboard/mouse automation for simulating actual typing and clicks on the user's machine.
- **PyQt5**: Implements a cross-platform graphical user interface for configuring typing speed, accuracy, and other race parameters.
- **JavaScript Userscript**: Runs in the browser, injecting itself onto supported sites (e.g. nitrotype.com), and extracts the required text and page elements via DOM interaction. Communicates with the Python backend to request typing automation and handles events such as reCAPTCHA challenges.

## Features

- Automated typing with adjustable Words Per Minute (WPM) and typing accuracy
- Graphical UI (PyQt5) for rapid configuration of race parameters
- Automated race sequence management (starting, stopping, advancing)
- reCAPTCHA position handling and click automation
- Cross-platform support: Windows and macOS
- Simple browser integration via userscript (such as via Tampermonkey)

## Requirements

- Python 3.x
- PyQt5
- Flask
- Flask-CORS
- PyAutoGUI
- Userscript manager (e.g. Tampermonkey for Chrome/Firefox)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/andruwsorensen/TheTypist2.0.git
   cd TheTypist2.0
   ```
2. Install the required Python packages:
   ```sh
   pip install PyQt5 Flask Flask-CORS pyautogui
   ```
3. Install the userscript located in this repository to your browser using a userscript manager (like Tampermonkey).

## Usage

1. Run the Python backend:
   ```sh
   python app.py
   ```
2. The PyQt5 GUI window will open, allowing you to set typing speed, accuracy, race count, and race timing.
3. Visit the supported typing website in your browser. The userscript will interface with the page and trigger automation via the backend.

## Configuration

The GUI lets you personalize:
- Time between races (seconds)
- Total number of races to automate
- Target WPM (Words Per Minute)
- Desired accuracy percentage
- reCAPTCHA click offsets

## How It Works

TheTypist2.0 comprises two major components:
1. **Python Backend** (`app.py`): Implements the automation logic, GUI interface, and Flask web server. It receives requests from the userscript, types out given text using PyAutoGUI, and handles clicks (e.g. reCAPTCHA).
2. **Browser Userscript** (`script.js`): Injects into typing-game pages, scrapes the text to be typed, detects race events, and communicates with the Flask backend for automation tasks.

## Contributing

Pull requests are welcome! Open issues or suggestions to improve the tool or add support for more games.

## Disclaimer

This tool is provided for educational and personal use. Do not use it to break terms of service of any websites. The developer is not responsible for misuse.
