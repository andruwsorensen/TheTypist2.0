from flask import Flask, request
from flask_cors import CORS
import pyautogui
import time
import random
import string

app = Flask(__name__)

# Constants/Settings for Race
TIME_BETWEEN_RACE = 2  # Seconds
AUTOMATE_RACES = True
RACE_COUNT = 100
WPM = 110
ACCURACY = 99  # in percent
CONTINUE_TYPING = True  # Global flag to control typing

# Set global delay in seconds
# pyautogui.PAUSE = 4 / WPM  # Equation to set delay based on WPM for Mac
pyautogui.PAUSE = 1 / (WPM * 10 / 60) # For windows

# Apply CORS with specific configuration
CORS(app)

@app.route('/type', methods=['POST'])
def type_text():
    global CONTINUE_TYPING
    CONTINUE_TYPING = True  # Reset typing flag
    data = request.json
    text = data['text']
    print("Text: " + text)  # Debug
    word_list = split_words(text, "\xa0")
    print_words(word_list)
    return 'Typed successfully', 200

def split_words(string, split_key):
    return string.split(split_key)

def print_words(word_list):
    global CONTINUE_TYPING
    longest_word = find_longest_word(word_list)
    print("The longest word is '" + longest_word + "' at " + str(len(longest_word)) + " letters.")

    for word in word_list:
        if not CONTINUE_TYPING:  # Check if typing should stop
            print("Typing stopped.")
            break

        if word == longest_word:
            pyautogui.press("enter")
            longest_word = ""
        else:
            for char in word:
                if not CONTINUE_TYPING:  # Check again before each character
                    print("Typing stopped.")
                    break

                adjust_for_accuracy()
                adjust_wpm()
                if char.isupper():
                    pyautogui.keyDown("shift")
                pyautogui.press(char)
                pyautogui.keyUp("shift")
            pyautogui.press("space")

def find_longest_word(word_list):
    return max(word_list, key=len)

def adjust_for_accuracy():
    if ACCURACY != 100:
        chance = random.random()
        wait_chance = random.random()
        if chance > ACCURACY / 100:
            pyautogui.press(random.choice(string.ascii_lowercase))
            if wait_chance > 0.75:
                time.sleep(1)

def adjust_wpm():
    wpm_temp = random.randint(WPM - 10, WPM + 10)
    # pyautogui.PAUSE = 4 / wpm_temp # For Mac
    pyautogui.PAUSE = 1 / (wpm_temp * 10 / 60) # For Windows

@app.route('/pause', methods=['POST'])
def pause_typing():
    global CONTINUE_TYPING
    CONTINUE_TYPING = False  # Set flag to stop typing
    print("Typing paused due to tab change or visibility loss.")
    return 'Typing paused', 200

@app.route('/next', methods=['POST'])
def next_race():
    global AUTOMATE_RACES
    global RACE_COUNT
    global CONTINUE_TYPING

    if AUTOMATE_RACES:
        print("Automate racing active.")
        RACE_COUNT -= 1
        print("There are " + str(RACE_COUNT) + " races left")
        time.sleep(TIME_BETWEEN_RACE)
        pyautogui.press("enter")
        if RACE_COUNT <= 1:
            AUTOMATE_RACES = False
        return 'On to next race', 200

    CONTINUE_TYPING = True  # Reset typing flag for the next race
    return 'No next race', 200

@app.route('/click', methods=['POST'])
def click_element():
    data = request.json
    print(data)
    x_coor = data['x']
    y_coor = data['y']

    # Add adjustable offsets
    x_offset = 130  # Adjust this value if needed
    y_offset = 180  # Adjust this value if needed
    
    # Apply offsets
    x_coor += x_offset
    y_coor += y_offset

    # Move the mouse to the reCAPTCHA checkbox
    pyautogui.moveTo(x_coor, y_coor, duration=0.5)  # Smoothly move the mouse

    # Pause for a brief moment to mimic natural behavior
    time.sleep(0.5)
    pyautogui.click()   
    time.sleep(1)
    pyautogui.click()

if __name__ == '__main__':
    app.run(port=5000)
