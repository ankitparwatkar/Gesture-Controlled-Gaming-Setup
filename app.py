import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
from selenium import webdriver
import threading
import time

# Page Config
st.set_page_config(page_title="Gesture-Controlled Subway Surf", page_icon="🎮", layout="wide")

# Custom Styles for Attractive UI
st.markdown("""
    <style>
        .big-text { font-size: 24px; font-weight: bold; color: #ff5722; }
        .button-style { background-color: #ff5722; color: white; padding: 15px; font-size: 22px; border-radius: 10px; }
        .container {
            text-align: center;
            background-color: #212121;
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(255, 87, 34, 0.8);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="container"><h1>🎮 Gesture-Controlled Subway Surf</h1></div>', unsafe_allow_html=True)
st.write("Raise fingers to control the game character!")

# Selenium Browser Setup to Launch Temple Run
def launch_game():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get("https://poki.com/en/g/subway-surfers")
    time.sleep(3)
    st.session_state["driver"] = driver
    st.success("Game launched! Click into the game before playing.")

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.85)
mp_draw = mp.solutions.drawing_utils

# Gesture Detection Function
def detect_gesture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        finger_count = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                finger_count = sum([1 for idx, lm in enumerate(hand_landmarks.landmark)
                                    if idx in [8, 12, 16, 20] and lm.y < hand_landmarks.landmark[idx - 2].y])

        st.image(frame, channels="BGR", width=480)
        perform_action(finger_count)

    cap.release()
    cv2.destroyAllWindows()

# Map Gestures to Game Controls
def perform_action(finger_count):
    actions = {1: 'up', 2: 'down', 3: 'right', 4: 'left'}
    if finger_count in actions:
        pyautogui.press(actions[finger_count])

# Function to Start Game & Gesture Control Together (Now runs both as separate threads)
def start_game():
    threading.Thread(target=launch_game, daemon=True).start()
    threading.Thread(target=detect_gesture, daemon=True).start()

# Streamlit Interactive Buttons
if st.button("🚀 Start Game & Gesture Control", help="Click to launch The Game and activate gesture tracking!", key="start_button"):
    start_game()
