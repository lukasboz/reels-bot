import pyautogui
import time
from pynput import keyboard

exit_flag = False

# === Callback for key press ===
def on_press(key):
    global exit_flag
    if key == keyboard.Key.alt_gr:  # Right Alt key
        exit_flag = True
        return False  # stop listener

# === Start keyboard listener ===
listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Move your mouse around. Press Right Alt to stop.\n")

try:
    while not exit_flag:
        x, y = pyautogui.position()
        position_str = f"X: {x} Y: {y}"
        print(position_str, end='', flush=True)
        print('\b' * len(position_str), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

print("\nDone.")
