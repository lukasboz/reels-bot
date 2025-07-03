import pyautogui
import time
import os
import shutil
from playsound import playsound

# === CONSTANTS ===
CAPCUT_WINDOW_TITLE = "CapCut"
INPUT_FILE = r"C:\Users\lukas\Github Projects\reels-bot\assets\input\tts_input.txt"
DOWNLOADS_FOLDER = r"C:\Users\lukas\Downloads"
DEST_FOLDER = r"C:\Users\lukas\Github Projects\reels-bot\assets\input"

# Voice to use (hardcoded)
VOICE_NAME = "Lukas-Clone"

def find_capcut_window():
    print("[INFO] Switching focus to CapCut...")
    windows = pyautogui.getWindowsWithTitle(CAPCUT_WINDOW_TITLE)
    if not windows:
        raise ValueError(f"CapCut window '{CAPCUT_WINDOW_TITLE}' not found.")
    capcut_window = windows[0]
    capcut_window.activate()
    time.sleep(1)

def input_text(text):
    print(f"[INFO] Typing text ({len(text)} characters)...")
    pyautogui.click(x=235, y=250)
    pyautogui.click(x=235, y=250)
    time.sleep(0.5)
    pyautogui.typewrite(text)

def select_voice(voice_name):
    print(f"[INFO] Selecting voice: {voice_name}...")
    voices = {
        "Lukas-Clone": (2000, 316),
    }
    if voice_name in voices:
        pyautogui.click(*voices[voice_name])
    else:
        raise ValueError(f"Voice '{voice_name}' not found.")

def generate_audio():
    print("[INFO] Generating audio...")
    pyautogui.click(x=2058, y=1380)
    time.sleep(30)

def export_audio():
    print(f"[INFO] Exporting audio to Downloads...")
    pyautogui.click(x=2014, y=437)
    time.sleep(0.5)
    pyautogui.click(x=1991, y=531)
    time.sleep(5)  # Wait for file to finish downloading

def move_latest_download():
    print("[INFO] Moving latest downloaded file to assets/input...")
    files = [os.path.join(DOWNLOADS_FOLDER, f) for f in os.listdir(DOWNLOADS_FOLDER)]
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        raise FileNotFoundError("No files found in Downloads folder.")

    latest_file = max(files, key=os.path.getmtime)

    # Generate unique filename based on timestamp and original extension
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    ext = os.path.splitext(latest_file)[1]
    new_filename = f"tts_output_{timestamp}{ext}"
    dest_path = os.path.join(DEST_FOLDER, new_filename)

    shutil.move(latest_file, dest_path)
    print(f"[INFO] Moved file to {dest_path}")


def main():
    try:
        if not os.path.exists(INPUT_FILE):
            raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
        
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            text_to_speak = file.read().strip()

        if not text_to_speak:
            raise ValueError("Input file is empty.")

        find_capcut_window()
        select_voice(VOICE_NAME)
        input_text(text_to_speak)
        generate_audio()
        export_audio()
        move_latest_download()

        print("[SUCCESS] TTS process completed successfully!")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
