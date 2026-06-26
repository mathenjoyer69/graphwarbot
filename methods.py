import matplotlib.pyplot as plt
import numpy as np
import pynput
import pyperclip
import threading

def sort_points(points):
    return sorted(points, key=lambda point: point[0][0])


def get_points(overlay, zz, tile_to_pixel):
    points = []
    funcs = ["double_abs", "step", "spike"]
    func_index = 0

    data_ready = threading.Event()

    overlay.root.after_idle(overlay.set_current_type, funcs[func_index])

    def calculation_thread():
        while True:
            data_ready.wait()
            data_ready.clear()

            curr_points = points.copy()
            if len(curr_points) < 2:
                continue

            points_c = sort_points(curr_points)
            x_vals, func_str = function_generator(points_c)
            y_vals = evaluate(func_str, x_vals)

            expected_start_y = points_c[0][0][1]
            dy = expected_start_y - y_vals[0]
            y_vals_corrected = y_vals + dy
            trans_points = translate_points(x_vals, y_vals_corrected, tile_to_pixel, zz)

            overlay.root.after_idle(overlay.set_points, trans_points)

    threading.Thread(target=calculation_thread, daemon=True).start()

    def on_click(x, y, button, pressed):
        if pressed:
            if button == pynput.mouse.Button.right:
                return False

            if button == pynput.mouse.Button.left:
                point = (x, y)
                point_relative = (point[0] - zz[0], zz[1] - point[1])
                point_tile = (point_relative[0] / tile_to_pixel, point_relative[1] / tile_to_pixel)

                points.append((point_tile, funcs[func_index]))
                overlay.root.after_idle(overlay.draw_circle, x, y)

                if len(points) > 1:
                    data_ready.set()

    def on_press(key):
        nonlocal points
        nonlocal func_index

        if key == pynput.keyboard.Key.backspace:
            if points:
                points = sort_points(points.copy())
                points.pop()
                overlay.root.after_idle(overlay.remove_last_circle)
                print(f"{points = }")

        if key == pynput.keyboard.Key.right:
            func_index = (func_index + 1) % len(funcs)
            print(f"currently selected: {funcs[func_index]}")
            overlay.root.after_idle(overlay.set_current_type, funcs[func_index])

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

def h_slope2(x1, y1, x2, y2):
    return (y2-y1)/(2*(x2-x1+1e-5))

def step(x: np.ndarray, a, h) -> np.ndarray:
    return h/(1+np.exp(-100*(x-a)))

def spike(x: np.ndarray, h, a) -> np.ndarray:
    return h/((np.pow((50*(x - a)), 2)) + 1)

def function_generator(point_function: list[tuple[tuple[float, float], str]]):
    if len(point_function) < 2:
        print("not enough points")
        return -1

    x_points = np.linspace(point_function[0][0][0], point_function[-1][0][0], 2000) #linspace between the first x to the last x values
    functions = []
    LNSI = 0  # LNSI = last_non_spike_index

    for i in range(1, len(point_function)):
        if point_function[i-1][1] != "spike":
            LNSI = i-1

        if point_function[i][1] == "double_abs":
            if point_function[i-1][1] == "spike":
                a = h_slope2(point_function[i-1][0][0], point_function[LNSI][0][1], point_function[i][0][0], point_function[i][0][1])
            else:
                a = h_slope(point_function[i-1][0], point_function[i][0])

            if i == 1:
                b = point_function[i - 1][0][0] + 0.2  # there is an offset so it wont skip it
            else:
                b = point_function[i - 1][0][0]

            c = point_function[i][0][0]

            func_string = f"{a:.2f}*(abs(x-{b:.2f})-abs(x-{c:.2f}))"
            functions.append(func_string)

        elif point_function[i][1] == "step":
            if point_function[i - 1][1] == "spike":
                h = point_function[i][0][1] - point_function[LNSI][0][1]
            else:
                h = point_function[i][0][1] - point_function[i - 1][0][1]

            if i == 1:
                a = point_function[i - 1][0][0] + 0.2  #there is an offset so it wont skip it
            else:
                a = point_function[i - 1][0][0]

            func_string = f"{h:.2f}/(1+exp(-100*(x-{a:.2f})))"
            functions.append(func_string)

        elif point_function[i][1] == "spike":
            if point_function[i - 1][1] == "spike":
                h = point_function[i][0][1] - point_function[LNSI][0][1]
            else:
                h = point_function[i][0][1] - point_function[i - 1][0][1]

            a = point_function[i][0][0]

            func_string = f"{h:.2f}/(((30*(x-{a:.2f}))^2)+1)"
            functions.append(func_string)

    all_funcs = "+".join(functions)
    all_funcs = all_funcs.replace("--", "+")
    all_funcs = all_funcs.replace("+-", "-")
    all_funcs = all_funcs.replace("-+", "-")
    print(all_funcs)
    pyperclip.copy(all_funcs)
    return x_points, all_funcs

def evaluate(func_string: str, x_points):
    func_string = func_string.replace("^", "**")
    func_string = func_string.replace("abs", "np.abs")
    func_string = func_string.replace("exp", "np.ezp")
    print(func_string)

    y_values = np.zeros(len(x_points))
    for i in range(len(x_points)):
        curr_func = func_string.replace("x", str(x_points[i]))
        curr_func = curr_func.replace("z", "x")
        y_point = eval(curr_func)
        y_values[i] = y_point

    return y_values

def translate_points(x_values: np.ndarray, y_values: np.ndarray, ttp, origin):
    x_pixels = x_values * ttp
    y_pixels = y_values * ttp

    relative_x = x_pixels + origin[0]
    relative_y = origin[1] - y_pixels
    points = np.column_stack((relative_x, relative_y))
    return points