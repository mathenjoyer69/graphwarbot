import tkinter as tk

class ScreenOverlay:
    def __init__(self, radius=15, type1="double_abs"):
        self.root = None
        self.canvas = None
        self.coords = []

        self.radius = radius
        self.type1 = type1

    def start(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black')

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.root.bind('<Escape>', lambda e: self.close())
        self.root.mainloop()

    def draw_circle(self, x, y):
        if self.canvas and self.root:
            self.coords.append((x, y))

            self.redraw()

    def remove_last_circle(self):
        if self.coords and self.canvas:
            self.coords.pop()

            self.redraw()

    def sort_coords(self):
        if self.coords:
            self.coords.sort(key=lambda point: point[0])

    def redraw(self):
        self.canvas.delete("all")
        self.sort_coords()
        if self.type1 == "double_abs":
            for i in range(1, len(self.coords)):
                prev_x, prev_y = self.coords[i - 1]
                curr_x, curr_y = self.coords[i]
                self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, fill='cyan', width=1)
        elif self.type1 == "step":
            for i in range(1, len(self.coords)):
                prev_x, prev_y = self.coords[i - 1]
                curr_x, curr_y = self.coords[i]
                self.canvas.create_line(prev_x, prev_y, prev_x, curr_y, fill='cyan', width=1)
                self.canvas.create_line(prev_x, curr_y, curr_x, curr_y, fill='cyan', width=1)

        for (cx, cy) in self.coords:
            self.canvas.create_oval(cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius, outline='cyan', width=2)

    def close(self):
        if self.root:
            self.root.quit()