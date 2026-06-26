import tkinter as tk
import numpy as np

class ScreenOverlay:
    def __init__(self, radius=15):
        self.root = None
        self.canvas = None
        self.points = []
        self.coords = []

        self.radius = radius
        self.type1 = "double_abs"
        self.current_type = "double_abs"

    def start(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black')

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.root.bind('<Escape>', lambda e: self.close())
        self.root.mainloop()

    def set_points(self, points1):
        self.points = points1
        self.redraw()

        if self.root:
            self.root.update()

    def draw_circle(self, x, y):
        if self.canvas and self.root:
            self.coords.append((x, y))
            self.redraw()

    def remove_last_circle(self):
        if self.points and self.canvas:
            self.points.pop()
            self.coords.pop()
            self.redraw()

    def set_current_type(self, new_type):
        self.current_type = new_type
        if self.canvas:
            self.redraw()

    def sort_points(self):
        if len(self.points) > 0:
            self.points = self.points[self.points[:, 0].argsort()]

        self.coords.sort(key=lambda point: point[0])

    def redraw(self):
        self.canvas.delete("all")
        self.sort_points()

        self.canvas.create_text(
            30, 30,
            text=f"active type: {self.current_type}",
            fill='cyan',
            font=('Arial', 18, 'bold'),
            anchor='nw'
        )

        for i in range(1, len(self.points)):
            curr_x, curr_y = self.points[i]
            prev_x, prev_y = self.points[i-1]

            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, fill='cyan', width=1)

        for point in self.coords:
            cx, cy = point
            self.canvas.create_oval(cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius, outline='cyan', width=2)

    def close(self):
        if self.root:
            self.root.quit()