from flask import Flask, request
from flask_cors import CORS
import pyautogui
import time
import random
import string
import platform
# New imports for PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys

app = Flask(__name__)

# Constants/Settings for Race
TIME_BETWEEN_RACE = 2  # Seconds
AUTOMATE_RACES = True
RACE_COUNT = 50
WPM = 100
ACCURACY = 99  # in percent
CONTINUE_TYPING = True  # Global flag to control typing

# New: Global dictionary to store current settings
current_settings = {
    'TIME_BETWEEN_RACE': TIME_BETWEEN_RACE,
    'RACE_COUNT': RACE_COUNT,
    'WPM': WPM,
    'ACCURACY': ACCURACY
}

# Set global delay in seconds
pyautogui.PAUSE = 1 / (WPM * 10 / 60) # For windows

# Apply CORS with specific configuration
CORS(app)

def adjust_pyautogui_pause(wpm):
    if wpm > 0:
        if platform.system() == "Darwin":  # macOS
            pyautogui.PAUSE = 60 / (wpm * 15.5)  # Adjusted for macOS
        else:  # Windows and others
            pyautogui.PAUSE = 1 / (wpm * 10 / 60)
    else:
        pyautogui.PAUSE = 0.1  # Default value if WPM is 0 or not set

# New: Flask thread class
class FlaskThread(QThread):
    def run(self):
        app.run(port=5000)

# New: Main window class for UI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing Automation Control")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_input_field("Time Between Race (s)", "time_between_race", TIME_BETWEEN_RACE)
        self.create_input_field("Race Count", "race_count", RACE_COUNT)
        self.create_input_field("WPM", "wpm", WPM)
        self.create_input_field("Accuracy (%)", "accuracy", ACCURACY)

        self.server_button = QPushButton("Start Server")
        self.server_button.clicked.connect(self.toggle_server)
        self.layout.addWidget(self.server_button)

        self.flask_thread = FlaskThread()
        self.server_running = False

        # Add a label to display races left
        self.races_left_label = QLabel(f"Races left: {current_settings['RACE_COUNT']}")
        self.layout.addWidget(self.races_left_label)

        # Connect textChanged signal to update_constants for each input field
        self.findChild(QLineEdit, "time_between_race").textChanged.connect(self.update_constants)
        self.findChild(QLineEdit, "race_count").textChanged.connect(self.update_constants)
        self.findChild(QLineEdit, "wpm").textChanged.connect(self.update_constants)
        self.findChild(QLineEdit, "accuracy").textChanged.connect(self.update_constants)

    def create_input_field(self, label_text, attribute_name, initial_value):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit(str(initial_value))
        input_field.setObjectName(attribute_name)
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.layout.addLayout(layout)

    def toggle_server(self):
        if not self.server_running:
            self.update_constants()
            self.flask_thread.start()
            self.server_button.setText("Stop Server")
            self.server_running = True
        else:
            # Implement a way to stop the Flask server (not trivial)
            self.server_button.setText("Start Server")
            self.server_running = False

    def update_constants(self):
        global current_settings

        try:
            time_between_race = self.findChild(QLineEdit, "time_between_race").text()
            current_settings['TIME_BETWEEN_RACE'] = float(time_between_race) if time_between_race else 2.0

            race_count = self.findChild(QLineEdit, "race_count").text()
            current_settings['RACE_COUNT'] = int(race_count) if race_count else 100

            wpm = self.findChild(QLineEdit, "wpm").text()
            current_settings['WPM'] = int(wpm) if wpm else 110

            accuracy = self.findChild(QLineEdit, "accuracy").text()
            current_settings['ACCURACY'] = float(accuracy) if accuracy else 99.0

            wpm = current_settings.get('WPM', 0)
            adjust_pyautogui_pause(wpm)

            # Update the races left label
            self.races_left_label.setText(f"Races left: {current_settings['RACE_COUNT']}")
        except ValueError as e:
            print(f"Error updating constants: {e}")
            # Optionally, you could show an error message to the user here

# Modified: Use current_settings instead of global variables
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

# Modified: Use current_settings instead of global ACCURACY
def adjust_for_accuracy():
    if current_settings['ACCURACY'] != 100:
        chance = random.random()
        wait_chance = random.random()
        if chance > current_settings['ACCURACY'] / 100:
            pyautogui.press(random.choice(string.ascii_lowercase))
            if wait_chance > 0.75:
                time.sleep(1)

# Modified: Use current_settings instead of global WPM
def adjust_wpm():
    wpm_temp = random.randint(current_settings['WPM'] - 10, current_settings['WPM'] + 10)
    adjust_pyautogui_pause(wpm_temp)

@app.route('/pause', methods=['POST'])
def pause_typing():
    global CONTINUE_TYPING
    CONTINUE_TYPING = False  # Set flag to stop typing
    print("Typing paused due to tab change or visibility loss.")
    return 'Typing paused', 200

# Modified: Use current_settings instead of global variables
@app.route('/next', methods=['POST'])
def next_race():
    global AUTOMATE_RACES
    global CONTINUE_TYPING

    if AUTOMATE_RACES:
        print("Automate racing active.")
        current_settings['RACE_COUNT'] -= 1
        print("There are " + str(current_settings['RACE_COUNT']) + " races left")
        
        # Update the races left label in the UI
        window.races_left_label.setText(f"Races left: {current_settings['RACE_COUNT']}")
        
        time.sleep(current_settings['TIME_BETWEEN_RACE'])
        pyautogui.press("enter")
        if current_settings['RACE_COUNT'] <= 1:
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
    x_offset = 300  # Adjust this value if needed
    y_offset = 280  # Adjust this value if needed
    
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

# Modified: New main block to run both PyQt and Flask
if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Start the Flask server in a separate thread
    flask_thread = FlaskThread()
    flask_thread.start()
    
    sys.exit(qt_app.exec_())