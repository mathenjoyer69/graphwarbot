import pyautogui
import numpy as np
import pynput
import pyperclip
import threading
from overlay import ScreenOverlay
import time

def sort_points(points):
    return sorted(points, key=lambda point: point[0])

def get_points(overlay, zz, tile_to_pixel):
    points = []
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
        nonlocal points

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
    return points

def double_abs(x: np.ndarray, a, b, c) -> np.ndarray:
    return a*(np.abs(x-b) - np.abs(x-c))

def h_slope(pos1, pos2):
    return (pos2[1]-pos1[1])/(2*(pos2[0]-pos1[0]+1e-5))

def step(x: np.ndarray, a, h) -> np.ndarray:
    h/(1+np.exp(-100*(x-a)))

def function_generator(player_pos_tile, other_points, type='double_abs'):
    if (len(other_points) < 2):
        print("not enough points")
        return -1

    x_points = np.linspace(player_pos_tile[0], other_points[-1][0], 2000)
    functions = []
    if type == 'double_abs':
        for i in range(1, len(other_points)):
            a = h_slope(other_points[i-1], other_points[i])
            b = other_points[i-1][0]
            c = other_points[i][0]
            points2 = double_abs(x_points, a, b, c)

            func_string = f"{a:.2f}*(abs(x-{b:.2f})-abs(x-{c:.2f}))"
            functions.append(func_string)
    elif type == "step":
        for i in range(1, len(other_points)):
            h = other_points[i][1] - other_points[i-1][1]
            if i == 1:
                a = other_points[i - 1][0] + 0.2 #could also be i and there is an offset so it wont skip it
            else:
                a = other_points[i - 1][0]
            try:
                points2 = step(x_points, a, h)
            except RuntimeError or OverflowError or RuntimeWarning:
                continue

            func_string = f"{h:.2f}/(1+exp(-100(x-{a:.2f})))"
            functions.append(func_string)

    all_funcs = "+".join(functions)
    all_funcs = all_funcs.replace("--", "+")
    all_funcs = all_funcs.replace("+-", "-")
    all_funcs = all_funcs.replace("-+", "-")
    print(all_funcs)
    pyperclip.copy(all_funcs)
    return x_points, points2, all_funcs