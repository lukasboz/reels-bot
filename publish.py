import pyautogui
import time
import os
import subprocess

# === SETTINGS ===
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
URL = "https://facebook.com/reels/create"
VIDEO_PATH = r"C:\Users\lukas\Github Projects\reels-bot\assets\output\gameplay_portrait.mp4"

subprocess.Popen([r"C:\Program Files\Mozilla Firefox\firefox.exe"])
time.sleep(3)  # Let browser open

pyautogui.hotkey('ctrl', 'l')  # Focus address bar
time.sleep(0.5)
pyautogui.typewrite(URL)
pyautogui.press('enter')
print("Navigating to:", URL)

time.sleep(3)  
pyautogui.click(x=2033, y=201)

time.sleep(2)
pyautogui.click(x=2067, y=587)
print("Clicked reel button")

time.sleep(7)

pyautogui.click(x=374, y=528)
time.sleep(3)

pyautogui.typewrite(VIDEO_PATH)
pyautogui.press('enter')
print("Selected file:", VIDEO_PATH)
time.sleep(5)

pyautogui.click(x=528, y=1334)
print("Clicked 'Next' button")
time.sleep(5)

pyautogui.click(x=374, y=528)
file_path = r"C:\Users\lukas\Github Projects\reels-bot\assets\input\tts_input.txt"

with open(file_path, 'r', encoding='utf-8') as f:
    first_line = f.readline().strip()  # .strip() removes \n

pyautogui.typewrite(first_line + ' #reddit #redditstorytime #narrator #story')

pyautogui.click(x=528, y=1334)
print("Clicked 'Next' button again")
time.sleep(5)

#PUBLISH



