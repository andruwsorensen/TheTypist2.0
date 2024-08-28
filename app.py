import subprocess
import sys

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["flask", "flask-cors", "pyautogui"]

# Install any missing packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# Now you can import the packages
from flask import Flask, request
from flask_cors import CORS
import pyautogui
import time
import random
import string

app = Flask(__name__)

# Constants/Settings for Race
TIME_BETWEEN_RACE = 3  # Seconds
AUTOMATE_RACES = True
RACE_COUNT = 30
WPM = 80
ACCURACY = 97  # in percent

# Set global delay in seconds
pyautogui.PAUSE = 4 / WPM  # Equation to set delay based on WPM

# Apply CORS with specific configuration
CORS(app, resources={r"/type": {"origins": "*"}}, supports_credentials=True)

@app.route('/type', methods=['POST'])
def type_text():
    data = request.json
    text = data['text']
    print("Text: " + text)  # Debug
    word_list = split_words(text, "\xa0")
    print_words(word_list)
    return 'Typed successfully', 200

def split_words(string, split_key):
    word_list = string.split(split_key)
    return word_list

def print_words(word_list):
    longest_word = find_longest_word(word_list)
    print("The longest word is '" + longest_word + "' at " + str(len(longest_word)) + " letters.")

    for word in word_list:
        if word == longest_word:
            pyautogui.press("enter")
            longest_word = ""
        else:
            for char in word:
                adjust_for_accuracy()
                adjust_wpm()
                if char.isupper():
                    pyautogui.keyDown("shift")
                pyautogui.press(char)
                pyautogui.keyUp("shift")
            pyautogui.press("space")

def find_longest_word(word_list):
    longest_word = max(word_list, key=len)
    return longest_word

def adjust_for_accuracy():
    if ACCURACY != 100:
        chance = random.random()
        if chance > ACCURACY / 100:
            pyautogui.press(random.choice(string.ascii_lowercase))

def adjust_wpm():
    wpm_temp = random.randint(WPM - 10, WPM + 10)
    pyautogui.PAUSE = 4 / wpm_temp

@app.route('/next', methods=['POST'])
def next_race():
    global AUTOMATE_RACES
    global RACE_COUNT
    if AUTOMATE_RACES:
        print("Automate racing active.")
        RACE_COUNT -= 1
        print("There are " + str(RACE_COUNT) + " races left")
        time.sleep(TIME_BETWEEN_RACE)
        pyautogui.press("enter")
        if RACE_COUNT <= 1:
            AUTOMATE_RACES = False
        return 'On to next race', 200
    return 'No next race', 200

if __name__ == '__main__':
    app.run(port=5000)
