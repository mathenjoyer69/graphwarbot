import pyautogui
import numpy as np
import pynput
import pyperclip
import threading
from overlay import ScreenOverlay
import time
import methods

zz = (938, 526) #zeor, zero -> screen coords
tile_to_pixel = 25.5
points = []
types = ["double_abs", "step"]
type_index = -1

def change_type():
    global type_index
    type_index = (type_index + 1) % len(types)

    def on_press(key):
        global type_index
        if key == pynput.keyboard.Key.right:
            type_index = (type_index + 1) % len(types)
            print(type_index)

        if key == pynput.keyboard.Key.down:
            return False

    keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    keyboard_listener.join()

change_type()
print(type_index)
overlay = ScreenOverlay(15, types[type_index])
overlay_thread = threading.Thread(target=overlay.start, daemon=True)
overlay_thread.start()

while overlay.root is None or overlay.canvas is None:
    time.sleep(0.1)

points = methods.get_points(overlay, zz, tile_to_pixel)
points = methods.sort_points(points)
print(points)


methods.function_generator(points[0], points, type=types[type_index])

