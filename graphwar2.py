import pyautogui
import numpy as np
import pynput
import pyperclip
import threading
from test import ScreenOverlay
import time

top_left = (302, 145)
bottom_right = (1576, 908)
zz = (938, 526)
tile_to_pixel = 25.5
points = []

overlay = ScreenOverlay()
overlay_thread = threading.Thread(target=overlay.start, daemon=True)
overlay_thread.start()

while overlay.root is None or overlay.canvas is None:
    time.sleep(0.1)

def sort_points(points):
    return sorted(points, key=lambda point: point[0])

def get_points():
    def on_click(x, y, button, pressed):
        if pressed:
            #right click to end the choosing phase
            if button == pynput.mouse.Button.right:
                return False

            if button == pynput.mouse.Button.left:
                point = (x, y)
                print(f"{point = }")
                point_relative = (point[0] - zz[0], zz[1] - point[1])
                point_tile = (point_relative[0] / tile_to_pixel, point_relative[1] / tile_to_pixel)
                print(f"{point_tile = }")
                points.append(point_tile)
                overlay.root.after_idle(overlay.draw_circle, x, y)

    def on_press(key):
        global points

        if key == pynput.keyboard.Key.backspace:
            if points:
                points = sort_points(points.copy())
                points.pop()
                overlay.root.after_idle(overlay.remove_last_circle)
                print(f"{points = }")

    mouse_listener = pynput.mouse.Listener(on_click=on_click)
    keyboard_listener = pynput.keyboard.Listener(on_press=on_press)

    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()

get_points()
points = sort_points(points)
print(points)

def doulbe_abs(x: np.ndarray, a, b, c) -> np.ndarray:
    return a*(np.abs(x-b) - np.abs(x-c))

def h_slope(pos1, pos2):
    return (pos2[1]-pos1[1])/(2*(pos2[0]-pos1[0]))

def function_generator(player_pos_tile, other_points, type='double_abs'):
    x_points = np.linspace(player_pos_tile[0], other_points[-1][0], 2000)
    functions = []
    if type == 'double_abs':
        for i in range(1, len(other_points)):
            a = h_slope(other_points[i-1], other_points[i])
            b = other_points[i-1][0]
            c = other_points[i][0]
            points2 = doulbe_abs(x_points, a, b, c)

            func_string = f"{a:.2f}*(abs(x-{b:.2f})-abs(x-{c:.2f}))"
            functions.append(func_string)

    all_funcs = "+".join(functions)
    all_funcs = all_funcs.replace("--", "+")
    all_funcs = all_funcs.replace("+-", "-")
    all_funcs = all_funcs.replace("-+", "-")
    print(all_funcs)
    pyperclip.copy(all_funcs)
    return x_points, points2

function_generator(points[0], points)

