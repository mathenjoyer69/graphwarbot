import threading
from overlay import ScreenOverlay
import time
import methods

zz = (960, 468)
tile_to_pixel = 15.38
points = []

overlay = ScreenOverlay(radius=10)
overlay_thread = threading.Thread(target=overlay.start, daemon=True)
overlay_thread.start()

while overlay.root is None or overlay.canvas is None:
    time.sleep(0.1)

points = methods.get_points(overlay, zz, tile_to_pixel)
points = methods.sort_points(points)
print(points)


methods.function_generator(points)