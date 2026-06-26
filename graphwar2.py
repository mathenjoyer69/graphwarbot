import threading
from overlay import ScreenOverlay
import time
import methods
import matplotlib.pyplot as plt

zz = (938, 526) #zero, zero -> screen coords
tile_to_pixel = 25.5
points2 = []

overlay = ScreenOverlay(radius=15)
overlay_thread = threading.Thread(target=overlay.start, daemon=True)
overlay_thread.start()

while overlay.root is None or overlay.canvas is None:
    time.sleep(0.1)

points2 = methods.get_points(overlay, zz, tile_to_pixel)
points2 = methods.sort_points(points2)
print(points2)


x_points, func = methods.function_generator(points2)

y_vals = methods.evaluate(func, x_points)
