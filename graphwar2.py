import pyautogui
import numpy as np
import pynput
import pyperclip

top_left = (302, 145)
bottom_right = (1576, 908)
zz = (938, 526)
tile_to_pixel = 25.5
points = []

def get_points():
    def on_click(x, y, button, pressed):
        if pressed:
            if button == pynput.mouse.Button.right:
                return False
            point = (x, y)
            print(f"{point = }")
            point_relative = (point[0] - zz[0], zz[1] - point[1])
            point_tile = (point_relative[0] / tile_to_pixel, point_relative[1] / tile_to_pixel)
            print(f"{point_tile = }")
            points.append(point_tile)

    with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()


get_points()
pptr = points[0]
print(f"{pptr = }")
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

            func_string = f"{a:.4f}*(abs(x-{b:.4f}) - abs(x-{c:.4f}))"
            functions.append(func_string)

    all_funcs = "+".join(functions)
    pyperclip.copy(all_funcs)
    return x_points, points2

function_generator(pptr, points)